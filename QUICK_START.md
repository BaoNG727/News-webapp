# ⚡ Quick Start Guide

## 🚀 Cách Nhanh Nhất (Windows)

### Bước 1: Cài Đặt Tự Động
```bash
# Chạy file setup.bat
setup.bat
```

Script sẽ tự động:
- ✅ Tạo virtual environment
- ✅ Cài đặt tất cả dependencies
- ✅ Tạo file .env
- ✅ Chạy database migrations
- ✅ Tạo superuser account

### Bước 2: Chạy Server
```bash
# Chạy file run.bat
run.bat
```

### Bước 3: Truy Cập
- 🌐 Frontend: http://127.0.0.1:8000/
- 🎛️ Admin Panel: http://127.0.0.1:8000/panel/
- 🔧 Django Admin: http://127.0.0.1:8000/admin/

---

## 📋 Các File .BAT Hữu Ích

| File | Mô Tả | Khi Nào Dùng |
|------|-------|--------------|
| `setup.bat` | Cài đặt dự án lần đầu | Chỉ chạy 1 lần khi mới clone project |
| `run.bat` | Chạy development server | Mỗi khi muốn start server |
| `migrate.bat` | Cập nhật database | Sau khi sửa models hoặc pull code mới |
| `test.bat` | Chạy tests | Kiểm tra code |
| `collectstatic.bat` | Thu thập static files | Trước khi deploy production |

---

## 🎯 Workflow Hàng Ngày

### Bắt Đầu Làm Việc
```bash
# 1. Pull code mới (nếu làm việc nhóm)
git pull origin main

# 2. Cập nhật database nếu cần
migrate.bat

# 3. Chạy server
run.bat
```

### Sau Khi Sửa Models
```bash
# Chạy migrations
migrate.bat

# Hoặc thủ công:
python manage.py makemigrations
python manage.py migrate
```

### Kết Thúc
- Nhấn `Ctrl+C` để dừng server
- Đóng terminal

---

## 🔑 Tài Khoản Mặc Định

Sau khi chạy `setup.bat`, bạn sẽ tạo superuser với:
- **Username**: (bạn chọn)
- **Email**: (bạn chọn)
- **Password**: (bạn chọn)

Dùng tài khoản này để login vào:
- Admin Panel: http://127.0.0.1:8000/panel/
- Django Admin: http://127.0.0.1:8000/admin/

---

## 📝 Tạo Bài Viết Đầu Tiên

### Cách 1: Qua Admin Panel
1. Login vào http://127.0.0.1:8000/panel/
2. Click "News" → "Add News"
3. Điền thông tin:
   - Title: "Bài viết đầu tiên"
   - Short Description: Mô tả ngắn
   - Content: Nội dung chi tiết
   - Upload ảnh
   - Chọn category
4. Click "Save" hoặc "Publish"

### Cách 2: Qua Django Admin
1. Login vào http://127.0.0.1:8000/admin/
2. Click "News Articles" → "Add News Article"
3. Điền thông tin tương tự
4. Click "Save"

---

## 🛠️ Xử Lý Lỗi Thường Gặp

### Lỗi: "No module named 'django'"
**Giải pháp:**
```bash
# Chạy lại setup
setup.bat
```

### Lỗi: "Port already in use"
**Giải pháp:**
```bash
# Dừng server đang chạy (Ctrl+C)
# Hoặc dùng port khác
python manage.py runserver 8080
```

### Lỗi: "Database is locked"
**Giải pháp:**
```bash
# Đóng tất cả kết nối đến database
# Restart server
run.bat
```

### Lỗi: "Static files not found"
**Giải pháp:**
```bash
collectstatic.bat
```

### Lỗi: "Image upload failed"
**Giải pháp:**
```bash
# Cài Pillow
pip install Pillow
```

---

## 📦 Cấu Trúc Thư Mục Quan Trọng

```
News-webapp/
│
├── 📂 media/          # Ảnh upload sẽ lưu ở đây
├── 📂 db.sqlite3      # Database file
├── 📂 venv/           # Virtual environment
│
├── 🔧 setup.bat       # Setup script
├── 🔧 run.bat         # Run server
├── 🔧 migrate.bat     # Database migrations
│
├── 📄 .env            # Cấu hình (tạo từ .env.example)
└── 📄 README.md       # Tài liệu chi tiết
```

---

## 🎨 Tùy Chỉnh

### Thay Đổi Logo & Tên Site
1. Login vào admin panel
2. Vào "Settings" → "Site Setting"
3. Upload logo và điền tên site
4. Click "Save"

### Thêm Category
1. Vào "Category" → "Category List"
2. Click "Add Category"
3. Nhập tên category
4. Click "Save"

### Thêm Trending News
1. Vào "Trending" → "Add Trending"
2. Chọn bài viết
3. Click "Save"

---

## 📚 Tài Liệu Chi Tiết

- 📖 [README.md](README.md) - Tài liệu đầy đủ
- 🎯 [IMPROVEMENTS.md](IMPROVEMENTS.md) - Tính năng mới
- 💾 [BACKUP_INSTRUCTIONS.md](BACKUP_INSTRUCTIONS.md) - Hướng dẫn backup

---

## 💡 Tips & Tricks

### 1. Auto-reload khi sửa code
Django development server tự động reload khi bạn sửa file `.py`. Chỉ cần:
- Sửa code
- Save file
- Refresh browser

### 2. Debug với print()
```python
def my_view(request):
    print("Debug:", variable)  # In ra terminal
    # Code của bạn
```

### 3. Shell để test code
```bash
python manage.py shell

>>> from news.models import News
>>> News.objects.all()
```

### 4. Xem SQL queries
```python
from django.db import connection
print(connection.queries)
```

---

## 🎓 Next Steps

Sau khi đã chạy được project:

1. ✅ Đọc [README.md](README.md) để hiểu chi tiết
2. ✅ Đọc [IMPROVEMENTS.md](IMPROVEMENTS.md) để biết tính năng mới
3. ✅ Tạo vài bài viết thử
4. ✅ Test các tính năng: search, comment, category
5. ✅ Tùy chỉnh template theo ý thích
6. ✅ Deploy lên production (nếu cần)

---

**Chúc bạn code vui vẻ! 🚀**
