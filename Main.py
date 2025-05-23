import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid 
import matplotlib.pyplot as plt
st.set_page_config(page_title = "KAJANG.ID")
file_orders = "orders.csv"
df = pd.DataFrame()
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
st.sidebar.title("KAJANG.ID")
if not st.session_state['logged_in']:
    with st.sidebar.expander("🔐 Login Penjual"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "Minjang" and password == "Minjang123":
                st.session_state['logged_in'] = True
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Username atau password salah!")
if st.session_state['logged_in']:
    menu = st.sidebar.radio("Pilih Halaman", ["📥 Update Stok", "📑 Pesanan","👤 Pelanggan", "📊 Laporan Penjualan","Logout"])
else:
    menu = st.sidebar.radio("Pilih Halaman", ["🏠 Beranda", "📦 Pemesanan", "🌟Tentang Kami","📬 Kontak Kami"])
if menu == "Logout":
    st.session_state['logged_in'] = False
    st.rerun()
col1, col2 = st.columns([1, 3])
with col1 :
    st.image("images/LOGO_KAJANG.png")
with col2 :
    st.title("KAJANG.ID")
    st.write("Sistem penjualan kacang panjang secara online")
if menu == "🏠 Beranda" :
    st.divider()
    st.subheader("HALAMAN UTAMA 🏠")
    st.write("KAJANG.ID merupakan sistem penjualan kacang panjang dalam mengelola penjualan secara efisien dan terstruktur. Sistem ini memudahkan pencatatan data penjualan, stok barang, harga, dan transaksi pelanggan secara online.")
    st.write("")
    st.info("Silahkan pilih menu di samping untuk mulai!")
    st.divider()
def baca_stok():
    df = pd.read_csv("stock.csv")
    stok = int(df[df["Produk"] == "Kacang Panjang"]["stok"].values[0])
    return stok
if menu == "📦 Pemesanan" :
    file_orders = "orders.csv"
    if os.path.exists(file_orders) and os.path.getsize(file_orders) > 0:
        try:
            df = pd.read_csv(file_orders)
            if "id_pesanan" not in df.columns:
                df["id_pesanan"] = [str(uuid.uuid4())[:4] for _ in range(len(df))]
                df.to_csv(file_orders, index=False)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=[
            "waktu", "nama", "Nomor Telepon", "jumlah", "alamat",
            "pilih metode pengiriman", "bukti pembayaran", "catatan tambahan", "total","id_pesanan",])
        df.to_csv(file_orders, index=False)
    if os.path.exists(file_orders) and os.path.getsize(file_orders) > 0:
        df = pd.read_csv(file_orders)
        if "id_pesanan" not in df.columns:
            df["id_pesanan"] = [str(uuid.uuid4())[:4] for _ in range(len(df))]
            df.to_csv(file_orders, index=False)
    file_orders = "orders.csv"
    st.divider()
    harga = 6000
    st.write("**Harga = 6000/iket**")
    st.write("**Silakan transfer ke rekening :**")
    st.write("**BCA-522020891 a.n KAJANG.ID**")
    st.divider()
    st.subheader("PESAN 📩")
    stok_tersedia = baca_stok()
    st.write(f"**Stok tersedia saat ini: {stok_tersedia} ikat**")
    stok_tersedia = baca_stok()
    with st.form("order_form") :
        name = st.text_input("Nama Anda")
        phone = st.text_input("Nomor Telepon")
        stok_tersedia = baca_stok()
        quantity = st.number_input("Jumlah (Perikat)", min_value=1, max_value=stok_tersedia, step=1)
        address = st.text_area("Alamat Pengiriman")
        delivery = st.selectbox("Pilih Metode Pengiriman", ["Ambil di tempat","Antar ke rumah"])
        total = quantity * harga
        total_pembayaran = st.write(f"Total: Rp {total:,}")
        bukti = st.file_uploader("Bukti Pembayaran", type=["jpg", "jpeg", "png"])
        notes = st.text_input("Catatan Tambahan")
        submitted = st.form_submit_button("Pesan Sekarang")
        if submitted:
            total = quantity * 6000
            if bukti is not None:
                id_pesanan = str(uuid.uuid4())[:4]
                st.image(bukti, caption="Bukti Pembayaran")
                folder_path = "uploads"
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, bukti.name)
                with open(file_path, "wb") as f:
                    f.write(bukti.getbuffer())
                    bukti_path = file_path
                    order = {
                        "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "nama": name,
                        "Nomor Telepon":phone,
                        "jumlah": quantity,
                        "alamat": address,
                        "pilih metode pengiriman":delivery,
                        "bukti pembayaran":bukti.name,
                        "catatan tambahan":notes,
                        "total": total,
                        "id_pesanan": id_pesanan,   }
                    df = pd.DataFrame([order])
                    file_exists = os.path.exists("orders.csv") and os.path.getsize("orders.csv") > 0
                    df.to_csv("orders.csv", mode='a', header=not file_exists, index=False)
                    stok_baru = stok_tersedia - quantity
                    df_stok = pd.read_csv("stock.csv")
                    df_stok.loc[df_stok["Produk"] == "Kacang Panjang", "stok"] = stok_baru
                    df_stok.to_csv("stock.csv", index=False)
                    st.success(f"✅ Pesanan berhasil atas nama **{name}** sebesar **Rp {total:,}**. \n\nID pesanan kamu: `{id_pesanan}`. Simpan ID ini untuk cek status.")
                    st.info("Simpan ID pesanan ini untuk cek status.")
            else:
                    st.warning("Mohon unggah bukti pembayaran sebelum melanjutkan.")
    st.subheader("Cek Status Pemesanan")
    kode = st.text_input("Masukkan ID Pesanan untuk Cek Status")
    cek_button = st.button("🔍 Cek Sekarang")
    
    file_orders = "orders.csv"
    hasil = pd.DataFrame()

    if cek_button:
        if os.path.exists(file_orders) and os.path.getsize(file_orders) > 0:
            df = pd.read_csv(file_orders)
        if kode:
            hasil = df[df["id_pesanan"].str.lower() == kode.lower()]
            if not hasil.empty:
                st.success("✅ Pesanan ditemukan:")
                st.dataframe(hasil)
            else:
                st.warning("❌ Pesanan tidak ditemukan.")
        else:
            st.warning("Masukkan ID pesanan terlebih dahulu.")
    st.info("Silakan masukkan nama atau kode untuk mengecek pesanan")

if menu == "🌟Tentang Kami":
    st.divider()
    st.subheader("Sejarah KAJANG.ID 🌱")
    st.write("KAJANG.ID merupakan aplikasi digital yang bergerak dalam bidang agrikultur, khususnya dalam pengelolaan dan pencatatan penjualan kacang panjang. Aplikasi ini pertama kali digagas sebagai bagian dari tugas mata kuliah Sistem Informasi Manajemen (SIM) oleh tiga mahasiswa: Aurora, Fathin, dan Natavia.")
    st.write("Didirikan pada tanggal 7 Mei 2025, dengan mengusung nilai inovatif, praktis, dan berdampak, KAJANG.ID tumbuh sebagai aplikasi agrikultur yang bukan hanya menjadi tugas akademik, tapi juga memiliki potensi untuk memberikan kontribusi langsung bagi masyarakat petani. ")
    st.divider()
    st.subheader("FAQ 💬") 
    faq = [{
        "question": "**Siapa saja yang bisa menggunakan KAJANG.ID**?",
        "answer": "Siapa saja bisa menggunakan KAJANG.ID, tetapi untuk pemesanan kacang panjang secara online hanya bisa dilakukan oleh konsumen yang berdomisili di Pati."},
        {
        "question": "**Apakah saya bisa mengedit atau membatalkan pesanan?**",
        "answer": "Sistem belum mendukung pengeditan atau pembatalan otomatis. Jika terjadi kesalahan hubungi admin melalui halaman kontak."},
        {
        "question": "**Bagaimana cara melakukan pembelian?**",
        "answer": "Masuk ke halaman pemesanan, isi data yang diminta, lalu klik pesan sekarang."}]
    for item in faq :
        with st.expander(item["question"]):
            st.write(item["answer"])
    st.divider()
if menu ==  "📬 Kontak Kami":
    st.subheader("✉ Hubungi Kami")
    st.markdown("Silakan hubungi kami melalui kontak berikut untuk pertanyaan, kerjasama, atau masukan:")
    st.divider()
    st.subheader("📞 Kontak Langsung")
    st.markdown("""
    - 📧 **Email:** [kajangid@gmail.com](mailto:kajangid@gmail.com)  
    - 📱 **WhatsApp:** [0857-1621-9108](https://wa.me/6285716219108)  
    - 📍 **Alamat:** Jl. Sekaran No.11, Gunung Pati, Semarang, Jawa Tengah""")
    st.divider()
    st.info("Kami akan merespons pesan Anda secepat mungkin pada jam kerja.")
if menu == "📥 Update Stok":
    st.divider()
    st.subheader("📥 Update Stok Kacang Panjang")
    try:
        df_stok = pd.read_csv("stock.csv")
        stok_saat_ini = int(df_stok[df_stok["Produk"] == "Kacang Panjang"]["stok"].values[0])
    except:
        df_stok = pd.DataFrame([{"Produk": "Kacang Panjang", "stok": 0}])
        stok_saat_ini = 0
    st.write(f"🔢 Stok saat ini: **{stok_saat_ini} ikat**")
    with st.form("form_update_stok"):
        opsi = st.radio("Pilih Jenis Update", ["Ganti total stok", "Tambah stok"])
        nilai = st.number_input("Jumlah stok", min_value=0, step=1)
        tombol = st.form_submit_button("Simpan")
        if tombol:
            if opsi == "Ganti total stok":
                df_stok.loc[df_stok["Produk"] == "Kacang Panjang", "stok"] = nilai
                st.success(f"✅ Stok berhasil diganti menjadi {nilai} ikat.")
            else:  
                stok_baru = stok_saat_ini + nilai
                df_stok.loc[df_stok["Produk"] == "Kacang Panjang", "stok"] = stok_baru
                st.success(f"✅ Stok berhasil ditambah {nilai} ikat. Total: {stok_baru} ikat.")           
            df_stok.to_csv("stock.csv", index=False)    
if menu == "📑 Pesanan":
    st.divider()
    st.subheader("📑 Daftar Pesanan Masuk")
    if os.path.exists("orders.csv") and os.path.getsize("orders.csv") > 0:
        df_orders = pd.read_csv("orders.csv")
        if "status" not in df_orders.columns:
            df_orders["status"] = "Baru"
        if df_orders.empty:
            st.info("Belum ada data pesanan.")
        else:
            st.dataframe(df_orders)
            st.subheader("🗑 Hapus Data Pesanan")
            id_hapus = st.selectbox("Pilih ID Pesanan untuk Dihapus", df_orders["id_pesanan"].unique())
            hapus_button = st.button("Hapus Pesanan")
            if hapus_button:
                df_orders = df_orders[df_orders["id_pesanan"] != id_hapus]
                df_orders.to_csv("orders.csv", index=False)
                st.success(f"Pesanan dengan ID {id_hapus} berhasil dihapus.")
            st.divider()
            st.subheader("🔁 Update Status Pesanan")
            selected_id = st.selectbox("Pilih ID Pesanan", df_orders["id_pesanan"].unique())
            new_status = st.selectbox("Pilih Status Baru", ["Baru", "Dikemas", "Dikirim", "Selesai"])
            if st.button("Update Status"):
                df_orders.loc[df_orders["id_pesanan"] == selected_id, "status"] = new_status
                df_orders.to_csv("orders.csv", index=False)
                st.success(f"Status pesanan {selected_id} berhasil diubah menjadi '{new_status}'.")
            st.divider()
            st.subheader("📜 Riwayat Transaksi")
            st.dataframe(df_orders.sort_values(by="waktu", ascending=False))
    else:
        st.warning("Belum ada pesanan masuk.")
if menu == "👤 Pelanggan":
    st.subheader("👤 Data Pelanggan")
    if os.path.exists("orders.csv") and os.path.getsize("orders.csv") > 0:
        df_orders = pd.read_csv("orders.csv")
        if "nama" not in df_orders.columns:
            st.warning("Kolom 'nama' tidak ditemukan di file orders.csv.")
        else:
            pelanggan_unik = df_orders["nama"].dropna().unique()
            st.write(f"Total pelanggan: {len(pelanggan_unik)}")
            st.dataframe(pd.DataFrame(pelanggan_unik, columns=["Nama Pelanggan"]))
            st.subheader("📜 Riwayat Belanja Pelanggan")
            selected_pelanggan = st.selectbox("Pilih Pelanggan", pelanggan_unik)
            riwayat = df_orders[df_orders["nama"] == selected_pelanggan]
            if not riwayat.empty:
                st.write(f"Total transaksi: {len(riwayat)}")
                st.dataframe(riwayat.sort_values(by="waktu", ascending=False))
            else:
                st.info("Pelanggan ini belum memiliki riwayat belanja.")
    else:
        st.warning("Belum ada data pesanan yang tersimpan.")
if menu == "📊 Laporan Penjualan":
   st.divider()
   st.subheader("LAPORAN KAJANG.ID")
   uploaded_file = st.file_uploader("Upload file orders.csv", type="csv")
   if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    data['waktu'] = pd.to_datetime(data['waktu'])    
    st.subheader("Data Penjualan (preview)")
    st.dataframe(data.head())
   
    total_omset = data['total'].sum()
    total_unit = data['jumlah'].sum()
    rata_penjualan = data.groupby('waktu')['total'].sum().mean()
    max_penjualan = data.groupby('waktu')['total'].sum().max()
    min_penjualan = data.groupby('waktu')['total'].sum().min()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Omset (Rp)", f"{total_omset:,}")
    col2.metric("Total Kacang Panjang Terjual (unit)", f"{total_unit}")
    col3.metric("Rata-rata Penjualan Harian (Rp)", f"{rata_penjualan:,.0f}")

    penjualan_harian = data.groupby('waktu')['total'].sum().reset_index()

    penjualan_harian['MA_7'] = penjualan_harian['total'].rolling(window=7).mean()

    st.subheader("Grafik Penjualan Harian dengan Moving Average 7 Hari")
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(penjualan_harian['waktu'], penjualan_harian['total'], label='Penjualan Harian', marker='o')
    ax.plot(penjualan_harian['waktu'], penjualan_harian['MA_7'], label='Moving Average 7 Hari', linewidth=3)
    ax.set_xlabel('waktu')
    ax.set_ylabel('Total Penjualan (Rp)')
    ax.legend()
    st.pyplot(fig)

    data['Bulan'] = data['waktu'].dt.to_period('M').astype(str)
    penjualan_bulanan = data.groupby('Bulan')['total'].sum().reset_index()
    if not penjualan_bulanan.empty:
        bulan_terbaik = penjualan_bulanan.loc[penjualan_bulanan['total'].idxmax()]
        st.metric("Bulan Penjualan Terbaik", bulan_terbaik['Bulan'], f"Rp {bulan_terbaik['total']:,.0f}")
    else:
        st.warning("Tidak ada data penjualan bulanan.")

    st.subheader("Penjualan Bulanan")
    st.bar_chart(penjualan_bulanan.set_index('Bulan'))
    if not penjualan_bulanan.empty:
        bulan_terbaik = penjualan_bulanan.loc[penjualan_bulanan['total'].idxmax()]
        st.metric("Bulan Penjualan Terbaik", bulan_terbaik['Bulan'], f"Rp {bulan_terbaik['total']:,.0f}")
        st.markdown(f"Bulan terbaik: {bulan_terbaik['Bulan']} dengan penjualan Rp {bulan_terbaik['total']:,}")
    else:
        st.warning("Data penjualan bulanan kosong. Tidak bisa menentukan bulan terbaik.")
    
    nama_hari_indonesia = {
    'Monday': 'Senin',
    'Tuesday': 'Selasa',
    'Wednesday': 'Rabu',
    'Thursday': 'Kamis',
    'Friday': 'Jumat',
    'Saturday': 'Sabtu',
    'Sunday': 'Minggu'}
    penjualan_hari = data.groupby(data['waktu'].dt.day_name())['total'].sum()
    penjualan_hari = penjualan_hari.rename(index=nama_hari_indonesia)
    if not penjualan_hari.empty:
        hari_terbaik = penjualan_hari.idxmax()
        st.subheader("Penjualan per Hari dalam Minggu")
        st.bar_chart(penjualan_hari)
        st.markdown(f"Hari terbaik: {hari_terbaik} dengan penjualan Rp {penjualan_hari[hari_terbaik]:,}")
    else:
        st.warning("Data penjualan per hari kosong.")
    
    st.subheader("Tabel Ringkasan Penjualan Bulanan")
    st.dataframe(penjualan_bulanan)












        
    