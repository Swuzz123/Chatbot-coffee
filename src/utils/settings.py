# utils/settings.py
mappings = {
  'Cà phê': {
    'Cà phê máy': ['Latte Classic', 'Latte Bạc Xỉu', 'Latte Coconut', 'Latte Hazelnut', 'Latte Caramel', 'Latte Almond', 'Latte Nóng'],
    'Cà phê phin': ['Bạc Xỉu Foam Dừa', 'Bạc Xỉu Caramel Muối', 'Đường Đen Sữa Đá','Bạc Xỉu Nóng',
                    'Bạc Xỉu', 'Cà Phê Sữa Đá', 'Cà Phê Đen Đá', 'Cà Phê Sữa Nóng', 'Cà Phê Đen Nóng'],
    'Cold Brew': ['Cold Brew Kim Quất', 'Cold Brew Sữa Tươi', 'Cold Brew Truyền Thống'],
    'A-Mê': ['A-Mê Tuyết Quất', 'A-Mê Tuyết Mơ', 'A-Mê Tuyết Đào', 'A-Mê Quất', 'A-Mê Mơ', 'A-Mê Đào', 'A-Mê Classic', 'Americano Nóng'],
    'Espresso': ['Espresso Đá','Cappuccino Đá', 'Caramel Macchiato Đá', 'Cappuccino Nóng', 'Caramel Macchiato Nóng', 'Espresso Nóng']
  },

  'Thức uống đá xay': {
    'Đá xay': ['Frosty Cà Phê Đường Đen', 'Frosty Caramel Arabica', 'Frosty Bánh Kem Dâu', 'Frosty Phin-Gato', 'Frosty Trà Xanh',
                'Frosty Cà Phê Đường Đen', 'Frosty Caramel Arabica', 'Frosty Phin-Gato', 'Frosty Trà Xanh', 'Frosty Bánh Kem Dâu'],
    'Đá xay có lớp whipping cream': ['Frappe Choco Chip', 'Frappe Hazelnut', 'Frappe Caramel', 'Frappe Almond', 'Frappe Espresso', 'Frappe Coconut Coffee', 'Frappe Matcha'],
  },

  'Matcha': {
    '': ['Matcha Yuzu Đá Xay', 'Matcha Yuzu', 'Matcha Đào Đá Xay', 'Matcha Đào', 'Matcha Okinawa Trân Châu Hoàng Kim', 'Matcha Sữa Dừa Đá Xay', 'Matcha Sữa Dừa',
        'Matcha Latte', 'Matcha Tinh Khiết', 'Trà Xanh - Xinh Chẳng Phai', 'Trà Xanh - Yêu Chẳng Phai', 'Matcha Latte Tây Bắc Sữa Yến Mạch', 'Trà Xanh Tây Bắc',
        'Matcha Latte Tây Bắc Sữa Yến Mạch (Nóng)', 'Trà Xanh Nước Dừa', 'Trà Xanh Nước Dừa Yuzu', 'Matcha Latte Tây Bắc (Nóng)', 'Matcha Latte Tây Bắc']
  },

  'Trà trái cây - Hi Tea': {
    'Hi Tea': ['Hi-Tea Yuzu Kombucha', 'Hi-Tea Đào Kombucha', 'Hi-Tea - Xinh Chẳng Phai', 'Hi-Tea Đào', 'Hi-Tea Vải', 'Hi-Tea Yuzu Trân Châu', 'Hi-Tea - Yêu Chẳng Phai',
                'Hi-Tea Đá Tuyết Mận Muối Trân Châu', 'Hi-Tea Dâu Tây Mận Muối Trân Châu', 'Hi-Tea Kim Quất Bưởi Hồng Mandarin', 'Dâu Phô Mai'],
    'Trà trái cây': ['Oolong Tứ Quý Sen',  'Oolong Tứ Quý Sen (Nóng)', 'Oolong Tứ Quý Dâu Trân Châu', 'Oolong Tứ Quý Vải',
                      'Oolong Tứ Quý Kim Quất Trân Châu', 'Trà Đào Cam Sả - Nóng', 'Trà Đào Cam Sả - Đá', 'Oolong Berry']
  },

  'Trà sữa': {
    '': ['Trà sữa Oolong Nướng Trân Châu', 'Trà Đen Macchiato', 'Hồng Trà Sữa Trân Châu', 'Hồng Trà Sữa Nóng',
        'Trà Sữa Oolong Tứ Quý Sương Sáo', 'Trà Sữa Oolong Nướng Sương Sáo','Trà Đào - Yêu Chẳng Phai',
        'Trà Sữa Oolong BLao', 'Trà sữa Oolong Nướng (Nóng)', 'Chocolate Nóng', 'Chocolate Đá']
  },

  'Bánh': {
    'Bánh ngọt': ['Mochi Kem Trà Sữa Trân Châu', 'Mochi Kem Matcha', 'Mochi Kem Chocolate', 'Mochi Kem Việt Quất', 'Mochi Kem Phúc Bồn Tử',
                  'Mousse Matcha', 'Mousse Tiramisu', 'Mousse Gấu Chocolate', 'Matcha Burnt Cheesecake', 'Burnt Cheesecake', 'Mít Sấy', 'Butter Croissant Sữa Đặc'],
    'Bánh mặn': ['Bánh Mì Que Bò Nấm Xốt Bơ', 'Bánh Mì Que Chà Bông Phô Mai Bơ Cay', 'Bánh Mì Que Pate Cột Đèn', 'Chà Bông Phô Mai', 'Croissant trứng muối', 'Butter Croissant']
  },

  'Đồ ăn chế biến': {
    '': ['Spaghetti Bò Bằm', 'Cơm Chiên Hải Sản']
  },

  'Cà phê gói mang đi': {
    '': ['Cà Phê Đen Đá Túi (30 gói x 16g)', 'Cà Phê Đen Đá Hộp (14 gói x 16g)', 'Cà Phê Hoà Tan Đậm Vị Việt (18 gói x 16 gam)',
        'Cà Phê Sữa Đá Hòa Tan Túi 25x22G', 'Cà Phê Rang Xay Original 1 250G', 'Cà Phê Sữa Đá Hòa Tan (10 gói x 22g)', 'Cà Phê Nguyên Hạt Arabica TCH (200gr)']
  }
}