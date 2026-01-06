from huggingface_hub import snapshot_download

print("Đang tải dataset...")
snapshot_download(
    repo_id="giahuy4205/traffic-detection",
    repo_type="dataset",
    local_dir="./dataset",
    local_dir_use_symlinks=False
)
print("Xong!")