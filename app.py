import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components
import requests

# ==========================================
# 1. KONFIGURASI & URL API GOOGLE SHEETS
# ==========================================
st.set_page_config(page_title="KaumPandak POS", page_icon="📍", layout="wide")

# URL WEB APP GOOGLE APPS SCRIPT ANDA
URL_GOOGLE_SCRIPT = "https://script.google.com/macros/s/AKfycbxkq3PxJimfMY6cxfRleQluYFuWXSaVz7inRfcblrWfsnw4V1L4OJfLaU_USUfbteUSAw/exec"

if 'role' not in st.session_state: st.session_state.role = None
if 'role_name' not in st.session_state: st.session_state.role_name = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'last_receipt' not in st.session_state: st.session_state.last_receipt = None
# db sementara untuk riwayat tampilan di sesi aktif kasir
if 'db_local' not in st.session_state: 
    st.session_state.db_local = pd.DataFrame(columns=['Waktu', 'Pos', 'Item', 'Pembayaran', 'Nominal'])

# ==========================================
# 2. DATABASE MENU LENGKAP
# ==========================================
MENU = {
    'Loket Motor': [
        {'name': 'Tiket Masuk Weekday', 'price': 25000, 'bidang': 'tiket motor'},
        {'name': 'Tiket Masuk Weekend/Libur', 'price': 30000, 'bidang': 'tiket motor'}
    ],
    'Loket Mobil': [
        {'name': 'Tiket Masuk Weekday', 'price': 25000, 'bidang': 'tiket mobil'},
        {'name': 'Tiket Masuk Weekend/Libur', 'price': 30000, 'bidang': 'tiket mobil'}
    ],
    'Cafe': [
        {'name': 'Kentang goreng', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Cireng', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Mix platter', 'price': 20000, 'bidang': 'cafe'}, {'name': 'Pempek', 'price': 20000, 'bidang': 'cafe'},
        {'name': 'Nasi goreng', 'price': 25000, 'bidang': 'cafe'}, {'name': 'Nasi ayam', 'price': 25000, 'bidang': 'cafe'},
        {'name': 'Spagheti', 'price': 20000, 'bidang': 'cafe'}, {'name': 'Bakso', 'price': 20000, 'bidang': 'cafe'},
        {'name': 'Mie Ayam biasa', 'price': 17000, 'bidang': 'cafe'}, {'name': 'Kwetiau', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Roti Bakar', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Cerpes 1 rasa', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Cerpes 2 rasa', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Kentang Tornado', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Burger', 'price': 12000, 'bidang': 'cafe'}, {'name': 'Dimsum', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Siomay', 'price': 17000, 'bidang': 'cafe'}, {'name': 'Seblak', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Odeng kuah', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Ice Cream', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Ice Cream Roti', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Sosis Bakar isi 1', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Sosis Bakar isi 2', 'price': 16000, 'bidang': 'cafe'}, {'name': 'Indomie Mi Goreng Rendang - Biasa', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Indomie Mi Goreng Rendang - + Telur', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Indomie Mi Goreng - Biasa', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Indomie Mi Goreng - + Telur', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Indomie Mi Kuah Ayam Bawang - Biasa', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Indomie Mi Kuah Ayam Bawang - + Telur', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Indomie Mi Kuah Kari Ayam - Biasa', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Indomie Mi Kuah Kari Ayam - + Telur', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Indomie Mi Kuah Soto - Biasa', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Indomie Mi Kuah Soto - + Telur', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Milky matcha', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Milky taro', 'price': 15000, 'bidang': 'cafe'}, {'name': 'Milky coklat', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Teh tarik - Hot', 'price': 10000, 'bidang': 'cafe'}, {'name': 'Teh tarik - Ice', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Gooday - Hot', 'price': 10000, 'bidang': 'cafe'}, {'name': 'Gooday - Ice', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Lemon tea - Hot', 'price': 10000, 'bidang': 'cafe'}, {'name': 'Lemon tea - Ice', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Teh manis - Hot', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Teh manis - Ice', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Teh tawar - Hot', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Teh tawar - Ice', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Indocafe - Hot', 'price': 10000, 'bidang': 'cafe'}, {'name': 'Indocafe - Ice', 'price': 15000, 'bidang': 'cafe'},
        {'name': 'Kapal api', 'price': 10000, 'bidang': 'cafe'}, {'name': 'Kopi liong', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Susu - Hot', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Susu - Ice', 'price': 10000, 'bidang': 'cafe'},
        {'name': 'Le mineral', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Pocari Sweat', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Milku Strawberry', 'price': 6000, 'bidang': 'cafe'}, {'name': 'Milku Coklat', 'price': 6000, 'bidang': 'cafe'},
        {'name': 'Golda', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Floridina', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Teh Pucuk', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Mizone', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Fruit Tea', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Teh Botol', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Teh Kotak', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Susu Ultra Strawberry', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Susu Ultra Coklat', 'price': 7000, 'bidang': 'cafe'}, {'name': 'Sprite Lemon', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Sprite Zero Sugar', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Isoplas Original', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Isoplas Coco', 'price': 7000, 'bidang': 'cafe'}, {'name': 'Larutan Penyegar Cap Badak 350ml', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Larutan Penyegar Cap Badak 200ml', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Larutan Penyegar Cap Kaki Tiga 200ml', 'price': 5000, 'bidang': 'cafe'},
        {'name': 'Pulpy Orange', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Coca Cola', 'price': 8000, 'bidang': 'cafe'},
        {'name': 'Nipis Madu', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Susu UHT Cimory Rasa Almond', 'price': 9000, 'bidang': 'cafe'},
        {'name': 'Susu UHT Cimory Rasa Hazelnut', 'price': 9000, 'bidang': 'cafe'}, {'name': 'Pop Mie Goreng', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Pop Mie Goreng Ayam Gledek', 'price': 12000, 'bidang': 'cafe'}, {'name': 'Pop Mie Kari Ayam', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Pop Mie Pedes Dower', 'price': 12000, 'bidang': 'cafe'}, {'name': 'Pop Mie Soto Ayam', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Pop Mie Ayam', 'price': 12000, 'bidang': 'cafe'}, {'name': 'Pop Mie Kari Lava', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Pop Mie Ayam Bawang', 'price': 12000, 'bidang': 'cafe'}, {'name': 'Pop Mie Baso', 'price': 12000, 'bidang': 'cafe'},
        {'name': 'Fanta', 'price': 8000, 'bidang': 'cafe'}, {'name': 'Susu UHT Cimory Rasa Marie Biscuit', 'price': 9000, 'bidang': 'cafe'},
        {'name': 'Aqua Mineral', 'price': 5000, 'bidang': 'cafe'}, {'name': 'Fresh tea Melati', 'price': 7000, 'bidang': 'cafe'},
        {'name': 'Ultra Taro', 'price': 7000, 'bidang': 'cafe'}, {'name': 'Es batu', 'price': 3000, 'bidang': 'cafe'},
        {'name': 'Air panas', 'price': 3000, 'bidang': 'cafe'}, {'name': 'Telur', 'price': 5000, 'bidang': 'cafe'},
        {'name': 'Nasi + Telur', 'price': 15000, 'bidang': 'cafe'}
    ],
    'Fasilitas_Ban': [
        {'name': 'KACAMATA BIASA', 'price': 15000, 'bidang': 'sewa ban'}, {'name': 'KACAMATA TEMPAT', 'price': 25000, 'bidang': 'sewa ban'},
        {'name': 'BAN ANAK', 'price': 30000, 'bidang': 'penjualan di ban'}, {'name': 'ROMPI PELAMPUNG', 'price': 35000, 'bidang': 'penjualan di ban'},
        {'name': 'Ban Hitam', 'price': 10000, 'bidang': 'sewa ban'}, {'name': 'Perahu', 'price': 30000, 'bidang': 'sewa ban'},
        {'name': 'Papan pelampung', 'price': 10000, 'bidang': 'sewa ban'}, {'name': 'Tikar', 'price': 20000, 'bidang': 'sewa karpet'},
        {'name': 'Matras', 'price': 15000, 'bidang': 'sewa karpet'}
    ],
    'Fasilitas_Loker': [
        {'name': 'Sewa Loker', 'price': 10000, 'bidang': 'sewa loker'}
    ],
    'Fasilitas_Gazebo': [
        {'name': 'Sewa Gazebo', 'price': 30000, 'bidang': 'Sewa Gazebo'}, {'name': 'Tambahan Sewa Gazebo', 'price': 10000, 'bidang': 'tambahan sewa gazebo'}
    ],
    'Campina': [
        {'name': 'Petit Semangka', 'price': 3000, 'bidang': 'Campina'}, {'name': 'Happy Cow Milky Tutti Fruitty', 'price': 5000, 'bidang': 'Campina'},
        {'name': 'Blue Lemonade', 'price': 5000, 'bidang': 'Campina'}, {'name': 'Hula-hula Kacang Ijo', 'price': 5000, 'bidang': 'Campina'},
        {'name': 'Hula-hula Alpukat', 'price': 5000, 'bidang': 'Campina'}, {'name': 'Korean Muscat', 'price': 5000, 'bidang': 'Campina'},
        {'name': 'Seoul Lychee', 'price': 5000, 'bidang': 'Campina'}, {'name': 'Cooky & Creamy (Oreo)', 'price': 5000, 'bidang': 'Campina'},
        {'name': 'Apple Fruitzy', 'price': 5000, 'bidang': 'Campina'}, {'name': 'Frozen', 'price': 6000, 'bidang': 'Campina'},
        {'name': 'Patrick', 'price': 6000, 'bidang': 'Campina'}, {'name': 'Spiderman', 'price': 6000, 'bidang': 'Campina'},
        {'name': 'Spongebobe Stick', 'price': 6000, 'bidang': 'Campina'}, {'name': 'Spongebobe Cup', 'price': 6000, 'bidang': 'Campina'},
        {'name': 'Heart Crunch', 'price': 8000, 'bidang': 'Campina'}, {'name': 'Concerto Midi Oreo', 'price': 6000, 'bidang': 'Campina'},
        {'name': 'Concerto Midi Strawberry', 'price': 6000, 'bidang': 'Campina'}, {'name': 'Tropicana Double Crunch', 'price': 7000, 'bidang': 'Campina'},
        {'name': 'Tropicana', 'price': 7000, 'bidang': 'Campina'}, {'name': 'Hula-hula Kacang Ijo Max', 'price': 7000, 'bidang': 'Campina'},
        {'name': 'Happy Cow Cup', 'price': 8000, 'bidang': 'Campina'}, {'name': 'Neapolitan', 'price': 10000, 'bidang': 'Campina'},
        {'name': 'Olympia choco vanilla', 'price': 7000, 'bidang': 'Campina'}, {'name': 'Fantazee choco milk', 'price': 5000, 'bidang': 'Campina'},
        {'name': 'My Cup Vanila cokelat mix', 'price': 5000, 'bidang': 'Campina'}, {'name': 'My Cup Choco Strawberry', 'price': 5000, 'bidang': 'Campina'}
    ],
    'Eskrim': [
        {'name': 'CUP ES KRIM', 'price': 5000, 'bidang': 'pos es krim'}, {'name': 'DJARUM COKLAT EXTRA', 'price': 19000, 'bidang': 'pos es krim'},
        {'name': 'DJARUM COKLAT', 'price': 20000, 'bidang': 'pos es krim'}, {'name': 'S MILD', 'price': 40000, 'bidang': 'pos es krim'},
        {'name': 'EVO', 'price': 28000, 'bidang': 'pos es krim'}, {'name': 'FILTER', 'price': 30000, 'bidang': 'pos es krim'},
        {'name': 'DJARUM SUPER', 'price': 26000, 'bidang': 'pos es krim'}, {'name': 'MAGNUM BINTANG', 'price': 28000, 'bidang': 'pos es krim'},
        {'name': 'MAGNUM HITAM', 'price': 28000, 'bidang': 'pos es krim'}, {'name': 'SAMSU', 'price': 25000, 'bidang': 'pos es krim'},
        {'name': 'CHIKI', 'price': 3000, 'bidang': 'pos es krim'}, {'name': 'SARI GANDUM', 'price': 3000, 'bidang': 'pos es krim'},
        {'name': 'NABATI', 'price': 3000, 'bidang': 'pos es krim'}, {'name': 'BATTER', 'price': 3000, 'bidang': 'pos es krim'},
        {'name': 'SLAI OLAY', 'price': 3000, 'bidang': 'pos es krim'}, {'name': 'SUPER STAR', 'price': 2000, 'bidang': 'pos es krim'},
        {'name': 'ISO PLUS', 'price': 7000, 'bidang': 'pos es krim'}, {'name': 'MILKU', 'price': 6000, 'bidang': 'pos es krim'},
        {'name': 'TEH PUCUK', 'price': 5000, 'bidang': 'pos es krim'}, {'name': 'MIZONE', 'price': 8000, 'bidang': 'pos es krim'},
        {'name': 'ULTRA TARO', 'price': 7000, 'bidang': 'pos es krim'}, {'name': 'NIPIS MADU', 'price': 5000, 'bidang': 'pos es krim'},
        {'name': 'SPRITE', 'price': 8000, 'bidang': 'pos es krim'}, {'name': 'TEH BOTOL (200ML)', 'price': 7000, 'bidang': 'pos es krim'},
        {'name': 'TEH BOTOL (250ML)', 'price': 8000, 'bidang': 'pos es krim'}, {'name': 'FLORIDINA', 'price': 5000, 'bidang': 'pos es krim'},
        {'name': 'POCARI', 'price': 8000, 'bidang': 'pos es krim'}, {'name': 'FANTA', 'price': 8000, 'bidang': 'pos es krim'},
        {'name': 'FRUIT TEA', 'price': 8000, 'bidang': 'pos es krim'}, {'name': 'AQUA', 'price': 5000, 'bidang': 'pos es krim'},
        {'name': 'Korek', 'price': 4000, 'bidang': 'pos es krim'}, {'name': 'Cimory', 'price': 9000, 'bidang': 'pos es krim'}
    ],
    'Kantin Belakang': [
        {'name': 'Popmie kari ayam - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie kari ayam - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie soto - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie soto - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie baso - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie baso - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie ayam bawang - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie ayam bawang - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie ayam - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie ayam - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie goreng - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie goreng - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie goreng geledek - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie goreng geledek - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie pangsit jontor - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie pangsit jontor - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie sedap ayam jerit - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie sedap ayam jerit - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Popmie Pedes Dower - Biasa', 'price': 12000, 'bidang': 'Kantin Belakang'}, {'name': 'Popmie Pedes Dower - + Telur', 'price': 17000, 'bidang': 'Kantin Belakang'},
        {'name': 'Indomie soto - Biasa', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Indomie soto - + Telur', 'price': 15000, 'bidang': 'Kantin Belakang'},
        {'name': 'Indomie ayam bawang - Biasa', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Indomie ayam bawang - + Telur', 'price': 15000, 'bidang': 'Kantin Belakang'},
        {'name': 'Indomie kari ayam - Biasa', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Indomie kari ayam - + Telur', 'price': 15000, 'bidang': 'Kantin Belakang'},
        {'name': 'Indomie rendang - Biasa', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Indomie rendang - + Telur', 'price': 15000, 'bidang': 'Kantin Belakang'},
        {'name': 'Indomie goreng - Biasa', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Indomie goreng - + Telur', 'price': 15000, 'bidang': 'Kantin Belakang'},
        {'name': 'Gooday - Hot', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Gooday - Ice', 'price': 10000, 'bidang': 'Kantin Belakang'},
        {'name': 'Kopi Kapal Api', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Kopi Liong', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Teh Tarik - Hot', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Teh Tarik - Ice', 'price': 10000, 'bidang': 'Kantin Belakang'},
        {'name': 'Kopi Mix - Hot', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Kopi Mix - Ice', 'price': 10000, 'bidang': 'Kantin Belakang'},
        {'name': 'Lemontea - Hot', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Lemontea - Ice', 'price': 10000, 'bidang': 'Kantin Belakang'},
        {'name': 'Susu Ultra Strawberry', 'price': 7000, 'bidang': 'Kantin Belakang'}, {'name': 'Susu Ultra Coklat', 'price': 7000, 'bidang': 'Kantin Belakang'},
        {'name': 'Susu Ultra Taro', 'price': 7000, 'bidang': 'Kantin Belakang'}, {'name': 'Milku Coklat', 'price': 6000, 'bidang': 'Kantin Belakang'},
        {'name': 'Milku Strawberry', 'price': 6000, 'bidang': 'Kantin Belakang'}, {'name': 'Golda Dolcelatte', 'price': 5000, 'bidang': 'Kantin Belakang'},
        {'name': 'Larutan', 'price': 5000, 'bidang': 'Kantin Belakang'}, {'name': 'Teh Botol (250ml)', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Teh Kotak', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Frutea', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Pocari Sweat', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Floridina', 'price': 7000, 'bidang': 'Kantin Belakang'},
        {'name': 'Pulpy', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Sprite', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Coca Cola', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Fanta', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Aqua 600mL', 'price': 5000, 'bidang': 'Kantin Belakang'}, {'name': 'Teh Pucuk', 'price': 5000, 'bidang': 'Kantin Belakang'},
        {'name': 'Cimory Almond', 'price': 9000, 'bidang': 'Kantin Belakang'}, {'name': 'Cimory Bisquit', 'price': 9000, 'bidang': 'Kantin Belakang'},
        {'name': 'Nipis Madu', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Teh Tawar', 'price': 5000, 'bidang': 'Kantin Belakang'},
        {'name': 'Es Batu', 'price': 4000, 'bidang': 'Kantin Belakang'}, {'name': 'Teh Manis panas', 'price': 8000, 'bidang': 'Kantin Belakang'},
        {'name': 'Teh Manis Es', 'price': 10000, 'bidang': 'Kantin Belakang'}, {'name': 'Air Panas', 'price': 3000, 'bidang': 'Kantin Belakang'},
        {'name': 'Frestea', 'price': 8000, 'bidang': 'Kantin Belakang'}, {'name': 'Ultra Mimi', 'price': 6000, 'bidang': 'Kantin Belakang'}
    ]
}

def login(role_key, role_name):
    if role_key == 'Admin':
        password = st.text_input("Password Admin", type="password")
        if st.button("Masuk"):
            if password == "admin123": 
                st.session_state.role = role_key
                st.session_state.role_name = role_name
                st.rerun()
            else:
                st.error("Password salah! Akses ditolak.")
    else:
        st.session_state.role = role_key
        st.session_state.role_name = role_name
        st.rerun()

# Fungsi untuk mengirim satu payload transaksi ke Google Apps Script (Web App)
def send_to_gsheets(payload):
    try:
        response = requests.post(URL_GOOGLE_SCRIPT, json=payload, timeout=15)
        return True, response.text
    except Exception as e:
        return False, str(e)

# ==========================================
# 3. HALAMAN LOGIN UTAMA
# ==========================================
if st.session_state.role is None:
    st.title("📍 KaumPandak Waterpark")
    st.write("Silakan pilih pos login Anda:")
    
    st.markdown("""
    <style>
    div.stButton > button:first-child { height: 60px; font-weight: bold; border-radius: 8px; font-size: 16px;}
    </style>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏢 Admin (Pemantauan)", use_container_width=True): login('Admin', 'Administrator Kantor')
        if st.button("🏊‍♂️ Ban / Loker / Gazebo", use_container_width=True): login('Ban / Loker / Gazebo', 'Ban / Loker / Gazebo')
        if st.button("🍲 Kantin Belakang", use_container_width=True): login('Kantin Belakang', 'Kantin Belakang')
    with c2:
        if st.button("🛵 Loket MOTOR", use_container_width=True): login('Loket Motor', 'Kasir Loket Motor')
        if st.button("🍦 Campina", use_container_width=True): login('Campina', 'Kasir Campina')
    with c3:
        if st.button("🚗 Loket MOBIL", use_container_width=True): login('Loket Mobil', 'Kasir Loket Mobil')
        if st.button("🍧 Pos Eskrim", use_container_width=True): login('Eskrim', 'Pos Eskrim')
        if st.button("🍔 Cafe", use_container_width=True): login('Cafe', 'Kasir Cafe')

# ==========================================
# 4. APLIKASI KASIR / ADMIN
# ==========================================
else:
    col_header, col_btn = st.columns([8, 2])
    col_header.title(f"📌 {st.session_state.role_name}")
    if col_btn.button("🚪 Ganti Pos / Logout", use_container_width=True):
        st.session_state.role = None
        st.session_state.cart = []
        st.session_state.last_receipt = None
        st.rerun()
        
    st.divider()

    # ----------------------------------------
    # A. PANEL ADMIN
    # ----------------------------------------
    if st.session_state.role == "Admin":
        st.subheader("Input Transaksi Admin")
        kategori = st.selectbox("Pilih Kategori Admin:", ["Khusus (Pembayaran di Kantor)", "Umum (Setoran Pos)"])
        
        bidang_khusus, bidang_umum = "", ""
        if "Khusus" in kategori:
            bidang_khusus = st.text_input("Nama Tiket Khusus / Bidang:")
        else:
            bidang_umum = st.selectbox("Pilih Pos Setoran:", ["pos 1", "pos 2", "pos 3", "pos 4", "pos 6", "pos 8", "pos 9", "pos 10", "pos 11", "pos 12"])
            
        keterangan = st.text_input("Keterangan Tambahan:")
        nominal = st.number_input("Nominal (Rp):", min_value=0, step=5000)
        pembayaran = st.radio("Jenis Pembayaran:", ["CASH", "QRIS", "TRANSFER"], horizontal=True)
        
        if st.button("Simpan Transaksi Admin ke GSheets", type="primary", use_container_width=True):
            if ("Khusus" in kategori and not bidang_khusus):
                st.error("Nama Tiket Khusus / Bidang wajib diisi!")
            else:
                payload = {
                    "pos": "Admin",
                    "kategori": "khusus" if "Khusus" in kategori else "umum",
                    "pembayaran": pembayaran,
                    "nominal": nominal,
                    "bidangUmum": bidang_umum,
                    "bidangKhusus": bidang_khusus,
                    "jumlah": 1,
                    "penanggungJawab": "Admin Kantor",
                    "keterangan": keterangan
                }
                
                with st.spinner('Menyimpan ke Google Sheets...'):
                    success, msg = send_to_gsheets(payload)
                    
                if success:
                    st.success("✓ Transaksi Admin berhasil disimpan di Google Sheets (Rekap otomatis berjalan)!")
                    st.session_state.db_local.loc[len(st.session_state.db_local)] = [
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Admin", bidang_khusus or bidang_umum, pembayaran, nominal
                    ]
                else:
                    st.error(f"Gagal menyimpan ke Google Sheets: {msg}")

    # ----------------------------------------
    # B. PANEL KASIR (TRANSAKSI POS)
    # ----------------------------------------
    else:
        col_form, col_cart = st.columns([1, 1])
        
        with col_form:
            st.subheader("Form Transaksi Pos")
            
            # Penanganan Kategori Khusus Ban/Loker/Gazebo
            pos_key = st.session_state.role
            if pos_key == 'Ban / Loker / Gazebo':
                sub_cat = st.selectbox("Pilih Kategori Fasilitas:", ["Ban", "Loker", "Gazebo"])
                pos_key = f"Fasilitas_{sub_cat}"
            
            items = MENU.get(pos_key, [])
            item_names = [f"{i['name']} - Rp {i['price']:,}" for i in items]
            
            selected_item_str = st.selectbox("Pilih Layanan / Barang:", item_names)
            qty = st.number_input("Jumlah (Qty):", min_value=1, value=1)
            pembayaran = st.radio("Jenis Pembayaran:", ["CASH", "QRIS", "TRANSFER"], horizontal=True)
            
            # Logika Khusus Loket (Langsung Proses & Hitung Parkir)
            if st.session_state.role in ['Loket Motor', 'Loket Mobil']:
                st.markdown("**Penambahan Parkir**")
                parkir_name = "Parkir Motor" if st.session_state.role == 'Loket Motor' else "Parkir Mobil"
                parkir_price = 2000 if st.session_state.role == 'Loket Motor' else 5000
                qty_parkir = st.number_input(f"Jumlah {parkir_name} (Rp {parkir_price:,}):", min_value=0, value=1)
                
                selected_idx = item_names.index(selected_item_str)
                item_data = items[selected_idx]
                total_harga = (item_data['price'] * qty) + (parkir_price * qty_parkir)
                
                st.error(f"Total Harus Dibayar: Rp {total_harga:,}")
                uang = st.number_input("Uang Dibayarkan Konsumen (Rp):", min_value=0, step=5000)
                
                if st.button("Proses & Simpan ke GSheets", type="primary", use_container_width=True):
                    if uang < total_harga:
                        st.error("Nominal uang pembayaran kurang dari total tagihan!")
                    else:
                        with st.spinner('Menyimpan transaksi ke Google Sheets...'):
                            # 1. Payload Tiket Utama
                            payload_tiket = {
                                "pos": st.session_state.role_name,
                                "kategori": "umum",
                                "pembayaran": pembayaran,
                                "nominal": item_data['price'],
                                "bidangUmum": item_data['bidang'],
                                "bidangKhusus": "",
                                "jumlah": qty,
                                "penanggungJawab": f"Kasir {st.session_state.role}",
                                "keterangan": item_data['name']
                            }
                            success, msg = send_to_gsheets(payload_tiket)
                            
                            # 2. Payload Parkir (Bila ada)
                            if qty_parkir > 0 and success:
                                payload_parkir = {
                                    "pos": st.session_state.role_name,
                                    "kategori": "umum",
                                    "pembayaran": pembayaran,
                                    "nominal": parkir_price,
                                    "bidangUmum": parkir_name.lower(),
                                    "bidangKhusus": "",
                                    "jumlah": qty_parkir,
                                    "penanggungJawab": f"Kasir {st.session_state.role}",
                                    "keterangan": parkir_name
                                }
                                success, msg = send_to_gsheets(payload_parkir)
                        
                        if success:
                            now = datetime.now()
                            # Record Struk
                            struk_items = f"{item_data['name']} ({qty}x) = Rp {item_data['price'] * qty:,}"
                            if qty_parkir > 0: 
                                struk_items += f"<br>{parkir_name} ({qty_parkir}x) = Rp {parkir_price * qty_parkir:,}"
                                
                            st.session_state.last_receipt = {
                                "pos": st.session_state.role_name,
                                "waktu": now.strftime("%d/%m/%Y %H:%M:%S"),
                                "items": struk_items,
                                "total": total_harga,
                                "bayar": uang,
                                "metode": pembayaran
                            }
                            # Simpan di local db UI
                            st.session_state.db_local.loc[len(st.session_state.db_local)] = [
                                now.strftime("%Y-%m-%d %H:%M:%S"), st.session_state.role_name, f"{item_data['name']} + Parkir", pembayaran, total_harga
                            ]
                            st.success(f"✓ Berhasil disimpan di Google Sheets! Kembalian: Rp {uang - total_harga:,}")
                        else:
                            st.error(f"Gagal mengirim ke Google Sheets: {msg}")
                        
            # Logika Pos Lain (Keranjang Belanja)
            else:
                if st.button("➕ Tambah ke Keranjang Pesanan", use_container_width=True):
                    selected_idx = item_names.index(selected_item_str)
                    item_data = items[selected_idx]
                    
                    st.session_state.cart.append({
                        "Item": item_data['name'],
                        "Bidang": item_data['bidang'],
                        "Harga": item_data['price'],
                        "Qty": qty,
                        "Subtotal": item_data['price'] * qty
                    })
                    st.rerun()
                    
        with col_cart:
            if st.session_state.role not in ['Loket Motor', 'Loket Mobil']:
                st.subheader("Keranjang Pesanan")
                if len(st.session_state.cart) == 0:
                    st.info("Belum ada item ditambahkan ke keranjang.")
                else:
                    cart_df = pd.DataFrame(st.session_state.cart)
                    st.dataframe(cart_df[['Item', 'Qty', 'Subtotal']], use_container_width=True)
                    
                    if st.button("🗑️ Kosongkan Keranjang"): 
                        st.session_state.cart = []
                        st.rerun()
                        
                    total_harga = cart_df['Subtotal'].sum()
                    st.error(f"Total Harus Dibayar: Rp {total_harga:,}")
                    uang = st.number_input("Uang Dibayarkan Konsumen (Rp):", min_value=0, step=5000)
                    
                    if st.button("Proses & Simpan ke GSheets", type="primary", use_container_width=True):
                        if uang < total_harga:
                            st.error("Nominal uang pembayaran kurang dari total tagihan!")
                        else:
                            now = datetime.now()
                            struk_items = []
                            is_success = True
                            
                            with st.spinner('Mengirim seluruh pesanan ke Google Sheets...'):
                                for item in st.session_state.cart:
                                    payload = {
                                        "pos": st.session_state.role_name,
                                        "kategori": "umum",
                                        "pembayaran": pembayaran,
                                        "nominal": item['Harga'],
                                        "bidangUmum": item['Bidang'],
                                        "bidangKhusus": "",
                                        "jumlah": item['Qty'],
                                        "penanggungJawab": f"Kasir {st.session_state.role}",
                                        "keterangan": item['Item']
                                    }
                                    
                                    success, msg = send_to_gsheets(payload)
                                    if not success:
                                        is_success = False
                                        st.error(f"Gagal mengirim item {item['Item']}: {msg}")
                                        break
                                    
                                    struk_items.append(f"{item['Item']} ({item['Qty']}x) = Rp {item['Subtotal']:,}")
                            
                            if is_success:
                                st.session_state.last_receipt = {
                                    "pos": st.session_state.role_name,
                                    "waktu": now.strftime("%d/%m/%Y %H:%M:%S"),
                                    "items": "<br>".join(struk_items),
                                    "total": total_harga,
                                    "bayar": uang,
                                    "metode": pembayaran
                                }
                                
                                st.session_state.db_local.loc[len(st.session_state.db_local)] = [
                                    now.strftime("%Y-%m-%d %H:%M:%S"), st.session_state.role_name, f"Keranjang ({len(st.session_state.cart)} item)", pembayaran, total_harga
                                ]
                                st.session_state.cart = []
                                st.success(f"✓ Seluruh pesanan berhasil masuk Google Sheets! Kembalian: Rp {uang - total_harga:,}")
                                st.rerun()

    # ----------------------------------------
    # C. FITUR CETAK STRUK
    # ----------------------------------------
    st.divider()
    if st.session_state.last_receipt and st.session_state.last_receipt['pos'] == st.session_state.role_name:
        st.subheader("Struk Transaksi Terakhir")
        r = st.session_state.last_receipt
        kembalian = r['bayar'] - r['total']
        
        html_struk = f"""
        <div style="border: 2px dashed #0277bd; padding: 15px; width: 350px; margin: auto; text-align: center; font-family: 'Courier New', Courier, monospace; background: #fafafa; border-radius: 8px;">
            <h3 style="margin: 0; color: #0277bd;">KAUMPANDAK WATERPARK</h3>
            <p style="margin: 5px 0; font-size:12px; font-weight: bold;">--- {r['pos'].upper()} ---</p>
            <p style="margin: 5px 0; font-size:12px;">Waktu: {r['waktu']}</p>
            <p style="margin: 5px 0; font-size:12px;">Metode: <b>{r['metode']}</b></p>
            <hr style="border: 1px dashed #000;">
            <div style="text-align: left; font-size:13px; font-weight: bold; margin: 10px 0; line-height: 1.6;">
                {r['items']}
            </div>
            <hr style="border: 1px dashed #000;">
            <div style="display:flex; justify-content:space-between; font-size: 15px; color: #d32f2f; font-weight: bold; margin-top:5px;">
                <span>TOTAL:</span>
                <span>Rp {r['total']:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size: 13px; margin-top:5px;">
                <span>BAYAR:</span>
                <span>Rp {r['bayar']:,}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size: 13px; margin-top:5px;">
                <span>KEMBALI:</span>
                <span>Rp {kembalian:,}</span>
            </div>
            <hr style="border: 1px dashed #000;">
            <p style="font-size:10px;">Terima Kasih Atas Kunjungan Anda!<br>~ Selamat Menikmati Liburan ~</p>
            <button onclick="window.print()" style="margin-top: 15px; padding: 12px; width: 100%; background: #2e7d32; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 5px; cursor: pointer;">🖨️ Cetak Struk Kasir</button>
        </div>
        """
        components.html(html_struk, height=500)

    # ----------------------------------------
    # D. RIWAYAT LOKAL SEMENTARA (Sesi Berjalan)
    # ----------------------------------------
    st.divider()
    st.subheader(f"Riwayat Sesi Aktif ({st.session_state.role_name})")
    
    current_db = st.session_state.db_local
    if st.session_state.role != "Admin":
        current_db = current_db[current_db["Pos"] == st.session_state.role_name]
        
    st.dataframe(current_db, use_container_width=True)
    
    col_stat1, col_stat2 = st.columns(2)
    col_stat1.info(f"Transaksi di Sesi Ini: {len(current_db)}")
    col_stat2.success(f"Omset Terkumpul di Sesi Ini: Rp {current_db['Nominal'].sum():,}")
