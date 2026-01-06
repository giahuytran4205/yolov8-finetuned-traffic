import os
import shutil
import random

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Thư mục gốc hiện tại (chứa images và labels)
source_root = r'D:\GHuy\Job\datasets\part_5_noido\part_5'

# Thư mục MỚI sẽ được tạo ra để chứa dữ liệu train/val
dest_root = r'D:\GHuy\Job\yolov8-fine-tuned\dataset'

# Tỉ lệ chia (0.8 = 80% Train, 20% Val)
train_ratio = 0.8 

def copy_and_split():
    # Định nghĩa đường dẫn nguồn
    src_images_dir = os.path.join(source_root, 'images')
    src_labels_dir = os.path.join(source_root, 'labels')

    # Kiểm tra thư mục nguồn
    if not os.path.exists(src_images_dir) or not os.path.exists(src_labels_dir):
        print("Lỗi: Không tìm thấy thư mục 'images' hoặc 'labels' trong source_root!")
        return

    # Lấy danh sách tên file (bỏ đuôi mở rộng) để khớp ảnh và nhãn
    # Hỗ trợ nhiều định dạng ảnh
    all_files = os.listdir(src_images_dir)
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.JPG', '.PNG'}
    
    # Lấy danh sách các file ID (tên file không đuôi)
    file_stems = [os.path.splitext(f)[0] for f in all_files if os.path.splitext(f)[1] in image_extensions]
    
    # Loại bỏ trùng lặp (nếu có file trùng tên khác đuôi) và xáo trộn
    file_stems = list(set(file_stems))
    random.shuffle(file_stems)
    
    # Tính toán số lượng
    train_count = int(len(file_stems) * train_ratio)
    
    print(f"Tổng số ảnh tìm thấy: {len(file_stems)}")
    print(f"Sẽ copy vào Train: {train_count} | Val: {len(file_stems) - train_count}")
    print(f"Đang xử lý... vui lòng chờ (đặc biệt nếu ảnh 4K nặng)")

    # Tạo cấu trúc thư mục đích
    for mode in ['train', 'val']:
        os.makedirs(os.path.join(dest_root, mode, 'images'), exist_ok=True)
        os.makedirs(os.path.join(dest_root, mode, 'labels'), exist_ok=True)

    # Bắt đầu Copy
    for i, stem in enumerate(file_stems):
        # Xác định mode
        mode = 'train' if i < train_count else 'val'
        
        # 1. Copy Ảnh
        # Cần tìm lại đúng đuôi file gốc
        found_img = False
        for ext in image_extensions:
            src_img_path = os.path.join(src_images_dir, stem + ext)
            if os.path.exists(src_img_path):
                dst_img_path = os.path.join(dest_root, mode, 'images', stem + ext)
                shutil.copy2(src_img_path, dst_img_path) # copy2 giữ nguyên metadata (ngày tháng tạo)
                found_img = True
                break
        
        # 2. Copy Nhãn
        src_txt_path = os.path.join(src_labels_dir, stem + '.txt')
        dst_txt_path = os.path.join(dest_root, mode, 'labels', stem + '.txt')
        
        if os.path.exists(src_txt_path):
            shutil.copy2(src_txt_path, dst_txt_path)
        elif found_img:
            # Trường hợp có ảnh mà không có label (ảnh background/negative sample)
            # Bạn có thể bỏ qua hoặc tạo file txt rỗng. Ở đây mình bỏ qua in cảnh báo.
            # print(f"Lưu ý: Ảnh {stem} không có file label.")
            pass

    print("\n" + "="*30)
    print("HOÀN TẤT!")
    print(f"Dữ liệu gốc tại '{source_root}' -> ĐÃ GIỮ NGUYÊN")
    print(f"Dữ liệu train tại '{dest_root}' -> ĐÃ SẴN SÀNG")

if __name__ == '__main__':
    copy_and_split()