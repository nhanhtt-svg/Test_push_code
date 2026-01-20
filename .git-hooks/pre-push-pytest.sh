#!/bin/bash

# Đọc input từ pre-push hook: mỗi line là "local_ref local_sha remote_ref remote_sha"
while read local_ref local_sha remote_ref remote_sha; do
    if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
        # Branch bị delete, không cần test
        continue
    fi
    if [ "$remote_sha" = "0000000000000000000000000000000000000000" ]; then
        # Branch mới, diff toàn bộ local_sha với origin (hoặc giả sử diff từ empty)
        changed_files=$(git log --name-only --pretty="format:" "$local_sha" | sort | uniq)
    else
        # Diff các file thay đổi giữa remote_sha và local_sha
        changed_files=$(git diff --name-only "$remote_sha" "$local_sha")
    fi

    # Kiểm tra nếu có thay đổi ở appA hoặc appB
    run_appA_tests=false
    run_appB_tests=false

    for file in $changed_files; do
        if [[ $file == appA/* ]]; then
            run_appA_tests=true
        fi
        if [[ $file == appB/* ]]; then
            run_appB_tests=true
        fi
    done

    # Chạy test chỉ cho phần thay đổi
    if [ "$run_appA_tests" = true ]; then
        echo "Running tests for appA..."
        python3 -m pytest tests/unit/appA -m 'not slow' -q --tb=short
        if [ $? -ne 0 ]; then exit 1; fi  # Nếu fail, stop push
    fi

    if [ "$run_appB_tests" = true ]; then
        echo "Running tests for appB..."
        python3 -m pytest tests/unit/appB -m 'not slow' -q --tb=short
        if [ $? -ne 0 ]; then exit 1; fi
    fi

    # Nếu không có thay đổi nào liên quan, có thể skip hoặc chạy minimum test
done

exit 0