# Backup Instructions

## Trước khi chạy migrations mới

### 1. Backup Database
```bash
# Copy file database
copy db.sqlite3 db.sqlite3.backup
```

### 2. Nếu có lỗi, restore database
```bash
# Xóa file hiện tại và restore
del db.sqlite3
copy db.sqlite3.backup db.sqlite3
```

### 3. Rollback migrations (nếu cần)
```bash
python manage.py migrate news zero
python manage.py migrate comment zero
```

## Sau khi backup thành công, chạy:
```bash
python manage.py makemigrations
python manage.py migrate
```
