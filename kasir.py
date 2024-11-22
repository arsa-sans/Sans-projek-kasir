import tkinter as tk
from tkinter import ttk, messagebox

class CoffeeShopSans:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Shop")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # data menu dan harga
        self.menu = {
            "KOPI": {
                "Americano": 15000,
                "Cappucino": 17000,
                "Espresso": 15500,
                "Latte": 15000,
                "Macchiato": 17500,
                "Affogato": 20000,
                "Cold Brew": 18000,
                "Caramel Macchiato": 22000,
                "Caramel Latte": 24000,
            },
            "MAKANAN": {
                "Kentang": 8000,
                "Churos": 5000,
                "Sosis": 5000,
                "Batagor": 10000,
                "Siomay": 10000,
                "Bakpao": 2500
            },
            "MINUMAN": {
                "Jus Apel": 8000,
                "Jus Mangga": 5000,
                "Jus Jeruk": 5000,
                "Jus Alpukat": 10000,
                "Jus Tomat": 5000,
                "Mojito": 5000
            }
        }

        # metode pembayaran
        self.metode_pembayaran = ["OVO", "Gopay", "Dana", "Tunai"]
        # inisiasi menu
        self.pesanan = []
        self.total = 0
        self.create_widgets()

    # membuat konten
    def create_widgets(self):
        # header menu
        tk.Label(self.root, text='Menu Barudak Ngopi', 
        bg="#F5DEB3",
        fg="#3D2B1F",
        font=('Times New Roman', 20, 'bold')).pack(pady=10)

        # membuat notebook
        notebook =  ttk.Notebook(self.root)
        notebook.pack(padx=5, pady=10, expand=True, fill='both')

        # membuat tab notebook untuk menu
        for category in self.menu:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)
            self.create_menu_button(frame, self.menu[category])

        # frame pesanan
        order_frame = ttk.Labelframe(self.root, height=5)
        order_frame.pack(pady=5, padx=5, fill='both')

        # listbox pesanan
        self.order_list = tk.Listbox(order_frame, height=8, bg="#EFDFBB")
        self.order_list.pack(padx=5, pady=5, fill='both')

        # label total
        self.total_label = tk.Label(order_frame, text='Total: Rp. 0', font=('Arial', 12))
        self.total_label.pack(pady=5)

        # tombol
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text='Bayar', command=self.checkout).pack(side='right')
        ttk.Button(button_frame, text='Hapus', command=self.clear_order).pack(side='right')

    # fungsi membuat tombol menu
    def create_menu_button(self, parent, menu_items):
        for i, (barang, harga) in enumerate(menu_items.items()):
            frame = ttk.Frame(parent)
            frame.grid(row=i//3, column=i%3, padx=5, pady=5)

            # menampilkan tombol untuk menu
            ttk.Label(frame, text=barang).pack()
            ttk.Label(frame, text=f'Rp {harga:,}').pack()
            ttk.Button(frame, text="Tambah", command=lambda item=barang, price=harga: self.menambah_pesanan(item, price)).pack()
    
    # fungis menambah pesanan
    def menambah_pesanan(self, item, price):
        self.pesanan.append((item, price))
        self.order_list.insert(tk.END, f'{item} - Rp. {price:,}')
        self.total += price
        self.total_label.config(text=f'Total: Rp {self.total:,}', font=('Times New Roman', 12, 'bold'), fg="#3D2B1F", bg="#F5DEB3")

    # fungsi menghapus orderan
    def clear_order(self):
        self.pesanan.clear()
        self.order_list.delete(0, tk.END)
        self.total = 0
        self.total_label.config(text="Total: Rp 0", font=('Times New Roman', 12, 'bold'), fg="#3D2B1F")

    # fungsi checkout
    def checkout(self):
        if not self.pesanan:
            messagebox.showwarning("Peringatan!", "Anda belum memesan")
            return
    
        # window checkout
        layar_checout = tk.Toplevel(self.root)
        layar_checout.title("Checkout")
        layar_checout.geometry("300x200")
        layar_checout.configure(bg="#F5DEB3")
        layar_checout.resizable(False, False)

        # form checkout / mengisi data nama untuk checkout
        ttk.Label(layar_checout, text="Nama : ", background="#F5DEB3", foreground="#3D2B1F", font=('Times New Roman', 15, 'bold')).pack(pady=5)
        nama_pemesan = ttk.Entry(layar_checout)
        nama_pemesan.pack(pady=5)

        # melilih metode pembayaran
        ttk.Label(layar_checout, text="Metode Pembayaran : ", background="#F5DEB3", foreground="#3D2B1F", font=('Times New Roman', 15, 'bold')).pack(pady=5)
        var_pembayaran = tk.StringVar()
        kombo_pembayaran = ttk.Combobox(layar_checout, textvariable=var_pembayaran, values=self.metode_pembayaran, state='readonly')
        kombo_pembayaran.pack(pady=5)

        # proses pembayaran
        def proses_pembayaran():
            nama = nama_pemesan.get().strip()
            pembayaran =  var_pembayaran.get()

            # kondisi dimana user tidak melengkapi data
            if not nama or not pembayaran:
                messagebox.showwarning("Peringatan!", "Mohon lengkapi data")
                return
            
            # membuat detail pesanan
            details = "\n".join(f"- {item}: Rp {price:,}" for item, price in self.pesanan)
            pesan = f'''
Nama Pemesan: {nama}
Metode Pembayaran: {pembayaran}

Detail Pesanan:
{details}

Total:  Rp {self.total:,}

Pesanan berhasil mohon tunggu sebentar.
'''
            
            # kondisi jika pesanan berhasil
            messagebox.showinfo('Sukses', pesan)
            layar_checout.destroy()
            self.clear_order()
        
        # tombol untuk bayar
        ttk.Button(layar_checout, text="Bayar", command=proses_pembayaran).pack(pady=10)

def main():
    root = tk.Tk()
    root.configure(bg="#F5DEB3")
    app = CoffeeShopSans(root)
    root.mainloop()

if __name__ == "__main__":
    main()
                                    

