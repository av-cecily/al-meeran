-- Initial Admin Data (password: admin123)
-- Hash generated using werkzeug.security.generate_password_hash('admin123')
INSERT IGNORE INTO admins (username, password) VALUES ('admin', 'scrypt:32768:8:1$pS6N1fW5D2W9W9W9$9f8b4d8e7c5b4a3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c');

-- Initial Products (Fabrics)
INSERT IGNORE INTO products (name, price, category, image_url) VALUES 
('Royal Silk', 0, 'Classic', 'static/assets/images/fabric-samples/royal-silk.jpg'),
('Premium Velvet', 0, 'Classic', 'static/assets/images/fabric-samples/premium-velvet.jpg'),
('Italian Leather', 0, 'Modern', 'static/assets/images/fabric-samples/italian-leather.jpg');
