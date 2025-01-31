# Fake Commit Github

## About this repository

- Dự án này dùng để làm giả các commit trên github theo mốc thời gian mà bạn muốn.
- Dự án này mình làm chỉ để cho vui thôi hehe ^^

## How to get the `GITHUB_TOKEN`

Để lấy một Personal Access Token (PAT) từ GitHub, bạn cần làm theo các bước sau đây. Token này sẽ cho phép bạn thực hiện các hoạt động trên GitHub thông qua API, chẳng hạn như tạo repository mới, push code, và nhiều thao tác khác tùy thuộc vào các quyền bạn cấp cho token.

- **Bước 1**: Đăng nhập vào GitHub
  - Mở trình duyệt của bạn và đăng nhập vào tài khoản GitHub của bạn tại github.com.
- **Bước 2**: Truy cập vào Settings
  - Sau khi đăng nhập, nhấp vào ảnh đại diện của bạn ở góc trên bên phải màn hình, sau đó chọn Settings từ menu thả xuống.
- **Bước 3**: Truy cập vào [Developer settings](https://github.com/settings/apps)
  - Trong trang cài đặt, cuộn xuống dưới cùng và chọn Developer settings ở cuối trang, nằm trong phần dành cho các tùy chỉnh nâng cao.
- **Bước 4**: [Personal Access Tokens](https://github.com/settings/tokens)
  - Trong menu bên trái của Developer settings, chọn Personal access tokens. Sau đó nhấp vào nút Generate new token ở góc trên bên phải của danh sách token hiện có (nếu có).
- **Bước 5**: Tạo Token [New Token](https://github.com/settings/tokens/new)
  - Đặt tên cho token của bạn trong trường Note để dễ nhận diện mục đích sử dụng của nó sau này.
  - Chọn thời gian hết hạn cho token trong phần Expiration. Bạn có thể chọn từ "No expiration" cho đến thời gian nhất định như 30 ngày, 90 ngày, v.v.
  - Chọn các quyền (scopes) mà bạn muốn cấp cho token. Để tạo và quản lý repositories, đảm bảo rằng bạn đã chọn repo. Bạn cũng có thể cần thêm các quyền khác tùy thuộc vào các hoạt động bạn dự định thực hiện qua API.
  - ![Permission](./resource/permission.png)
    Nhấp vào Generate token.
- **Bước 6**: Sao chép Token
  - Sau khi token được tạo, GitHub sẽ hiển thị cho bạn một lần duy nhất. Hãy chắc chắn sao chép token này và lưu nó một cách an toàn. Bạn không thể xem lại token sau khi rời khỏi trang này.
  - Sử dụng token này thay cho mật khẩu khi bạn truy cập GitHub qua API hoặc các công cụ dòng lệnh.

## Install

- Install `python`
- Download this repository [Download](https://github.com/shr3wcl/fake-git-commit/archive/refs/heads/main.zip)
- Install all of library: `pip install -r requirements.txt`
- Run it with command: `python app.py`
- Enjoy it ^^
