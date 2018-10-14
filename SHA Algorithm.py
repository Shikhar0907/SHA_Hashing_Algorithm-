from tkinter import *
from tkinter import filedialog

class App():

    
    def __init__(self):
        self.root = Tk()
        self.root.title("SHA")
        self.root.geometry("400x400")
        
    def read_file(self):
        label = Label(self.root,text="Please select the file").pack()
        self.root.filename = filedialog.askopenfilename(filetypes=[("All files","*.*")])
        self.root.title(self.root.filename)
        read_content = open(self.root.filename).read()
        text_box = Text(self.root, height = 10, width = 30)
        text_box.pack()
        text_box.insert(END,read_content)
        convert_button = Button(self.root,text="Convert to bits")
        convert_button.pack()
        convert_button.config(command=lambda: self.convert_to_bits(read_content))

    def convert_to_bits(self,read_content):
        bits_content = "0" + '0'.join(format(ord(i),'b') for i in read_content)
        bits_converted_content_label = Label(self.root,text=bits_content).pack()
        reserve_message = len(bits_content)
        bits_reserve_message = bin(reserve_message)
        bits_reserve_message = list(bits_reserve_message)
        del bits_reserve_message[1]
        print(bits_reserve_message)
        self.add_one(bits_content,bits_reserve_message)

    def add_one(self,bits_content,bits_reserve_message):
        bits_content = bits_content+"1"
        print(bits_content)
        self.add_zero(bits_content,bits_reserve_message)

    def add_zero(self,bits_content,bits_reserve_message):
        bits_content = list(bits_content)
        zero = 448 - len(bits_content)
        for i in range(zero):
            bits_content.append('0')
        end_bits = 512 - len(bits_content)
        last_zero = end_bits - len(bits_reserve_message)
        for i in range(last_zero):
            bits_content.append('0')
        for i in range(len(bits_reserve_message)):
                       bits_content.append(bits_reserve_message[i])
        print(len(bits_content))
        print(bits_reserve_message)
        self.split_32_block(bits_content)
        
    def split_32_block(self,bits_content):
        len_content = len(bits_content)/ 32
        j = 0
        block_content = []
        for i in range(int(len_content)):
            block_content.append(''.join(bits_content[j:j+32]))
            j = j+32
            i = i+1
        print(block_content)
        self.Main_loop(block_content)

    def Main_loop(self,block_content):
        Initial_hash = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]
        H1,H2,H3,H4,H5,H6,H7,H8 = map(int,Initial_hash)
        a,b,c,d,e,f,g,h = map(int,Initial_hash)
        K256 = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
                ]
        k256 = list(map(int,K256))
        w = []
        
        for i in range(0,64):
            if (i<16):
                w.append(int(block_content[i],2))
            
                T1 = (h + self.shifting1(e) + self.choose(e,f,g) + k256[i] + w[i])
                T2 = (self.shifting0(a) + self.Majority(a,b,c))
                h = g
                g = h
                f = e
                e = d + T1
                d = c
                c = b
                b = a
                a = T1 + T2
                H1 = a+H1
                H2 = b+H2
                H3 = c+H3
                H4 = d+H4
                H5 = e+H5
                H6 = f+H6
                H7 = g+H7
                H8 = h+H8
                print("Hash is :",(i,hex(H1),hex(H2),hex(H3),hex(H4),hex(H5),hex(H6),hex(H7),hex(H8)))

            else:
                W = self.gamma1(w[i-2]) + w[i-7] + self.gamma0(w[i-15]) + w[i-16]
                w.append(W)
                T1 = (h + self.shifting1(e) + self.choose(e,f,g) + k256[i] + W)
                T2 = (self.shifting0(a) + self.Majority(a,b,c))
                h = g
                g = h
                f = e
                e = d + T1
                d = c
                c = b
                b = a
                a = T1 + T2
                H1 = a+H1
                H2 = b+H2
                H3 = c+H3
                H4 = d+H4
                H5 = e+H5
                H6 = f+H6
                H7 = g+H7
                H8 = h+H8
                print("Hash is :",(i,hex(H1),hex(H2),hex(H3),hex(H4),hex(H5),hex(H6),hex(H7),hex(H8)))

        
    
        
    def choose(self,e,f,g):
        return ((e&f)^(~e&g))

    def Majority(self,a,b,c):
        return ((a&b)^(a&c)^(b&c))

    def shifting1(self,e):
        return (self.rotate_right(e,6) ^ self.rotate_right(e,11) ^ self.rotate_right(e,25))

    def shifting0(self,a):
        return (self.rotate_right(a,2) ^ self.rotate_right(a,13) ^ self.rotate_right(a,22))
                
    def rotate_right(self,e,n):
        BITS_IN_WORD = 32
        return (((e & 0xffffffff) >> (n & 31)) | (e << (BITS_IN_WORD - (n & 31)))) & 0xffffffff

    def gamma0(self,w):
        return (self.rotate_right(w, 7) ^ self.rotate_right(w, 18) ^ self.shift_right(w, 3))
    def gamma1(self,w):
        return (self.rotate_right(w, 17) ^ self.rotate_right(w, 19) ^ self.shift_right(w, 10))
    def shift_right(self,w,n):
        return (w & 0xffffffff) >> n
        
        
          
        
Call = App()
Call.read_file()
        
     





