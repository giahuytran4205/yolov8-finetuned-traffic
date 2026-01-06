import torch
from ultralytics import YOLO

# Bắt buộc phải có block này để tránh lỗi đa luồng (multiprocessing)
if __name__ == '__main__':
    
    # --- TỰ ĐỘNG PHÁT HIỆN GPU ---
    # Kiểm tra xem có bao nhiêu GPU
    gpu_count = torch.cuda.device_count()
    
    if gpu_count > 0:
        # Tạo danh sách ID: ví dụ có 4 GPU thì devices = [0, 1, 2, 3]
        devices = list(range(gpu_count))
        print(f"👉 Tìm thấy {gpu_count} GPU. Đang kích hoạt các device: {devices}")
    else:
        # Nếu không có GPU thì chạy CPU
        devices = 'cpu'
        print("👉 Không tìm thấy GPU. Chuyển sang chạy CPU.")

    # --- KHỞI TẠO VÀ TRAIN ---
    model = YOLO('yolov8n.pt') 

    results = model.train(
        data='data.yaml',
        epochs=30,
        imgsz=640,
        
        # Truyền danh sách device vừa tạo vào đây
        device=devices, 
        
        # QUAN TRỌNG: Tăng batch size lên
        # Nếu 1 GPU chịu được batch 16, thì 4 GPU nên để batch = 16 * 4 = 64
        batch=16 * gpu_count if gpu_count > 0 else 16,
        
        freeze=10  # (Tùy chọn) Freeze backbone nếu cần
    )