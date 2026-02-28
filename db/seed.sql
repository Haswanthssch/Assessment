-- ============================================================
--  Seed Data — Inventory & Order Management System
-- ============================================================

-- Admin user (password: admin123)
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@admin.com',
 '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uhlW',
 'admin')
ON CONFLICT (email) DO NOTHING;

-- Regular users (password: user123)
INSERT INTO users (username, email, password_hash, role) VALUES
('alice', 'alice@example.com',
 '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2uHeX1hVo6e',
 'user'),
('bob', 'bob@example.com',
 '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2uHeX1hVo6e',
 'user')
ON CONFLICT (email) DO NOTHING;

-- Products
INSERT INTO products (name, description, price, category, image_url) VALUES
('Laptop Pro 15',    'High-performance laptop with 16GB RAM',        999.99, 'Electronics',
 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'),
('Wireless Mouse',   'Ergonomic wireless mouse with 2.4GHz receiver',  29.99, 'Electronics',
 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400'),
('Mechanical Keyboard','RGB backlit mechanical keyboard 104 keys',      89.99, 'Electronics',
 'https://images.unsplash.com/photo-1541140532154-b024d705b90a?w=400'),
('Office Chair',     'Ergonomic office chair with lumbar support',    349.99, 'Furniture',
 'https://images.unsplash.com/photo-1589384267710-7a170981ca78?w=400'),
('Standing Desk',    'Height-adjustable standing desk 140x70cm',      499.99, 'Furniture',
 'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400'),
('USB-C Hub',        '7-in-1 USB-C hub with 4K HDMI output',           49.99, 'Electronics',
 'https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=400'),
('Monitor 27"',      '4K IPS display 27" with HDR support',           449.99, 'Electronics',
 'https://images.unsplash.com/photo-1547082299-de196ea013d6?w=400'),
('Notebook A5',      'Premium hard-cover ruled notebook 200 pages',     12.99, 'Stationery',
 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400'),
('Pen Set',          'Set of 12 premium ballpoint pens',                 8.99, 'Stationery',
 'https://images.unsplash.com/photo-1583485088034-697b5bc36b08?w=400'),
('Desk Lamp',        'LED desk lamp with adjustable brightness',        39.99, 'Furniture',
 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400')
ON CONFLICT DO NOTHING;

-- Inventory (product_id 1..10)
INSERT INTO inventory (product_id, quantity, reorder_level)
SELECT id, (RANDOM() * 100 + 10)::INT, 10
FROM products
ON CONFLICT (product_id) DO NOTHING;
