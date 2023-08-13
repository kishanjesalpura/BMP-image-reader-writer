class Image():

    def __init__(self, file_name):
        self.readBMP(file_name)


    def readBMP(self, file):
        with open(file, "rb") as img:

            # Reading file header
            # Check if Bitmap file
            self.sign = img.read(2).decode("ascii")
            if self.sign != "BM":
                return None
            
            self.file_size = int.from_bytes(img.read(4), "little")
            self.reserved = int.from_bytes(img.read(4), "little")
            self.d_offset = int.from_bytes(img.read(4), "little")

            # Reading BMP Header
            self.hdr_size = int.from_bytes(img.read(4), "little")
            self.width = int.from_bytes(img.read(4), "little")
            self.height = int.from_bytes(img.read(4), "little")
            self.planes = int.from_bytes(img.read(2), "little")
            self.bits_per_pixel = int.from_bytes(img.read(2), "little")
            self.compression = int.from_bytes(img.read(4), "little")
            self.image_size = int.from_bytes(img.read(4), "little")
            self.XpixelsperM = int.from_bytes(img.read(4), "little")
            self.YpixelsperM = int.from_bytes(img.read(4), "little")
            self.colors_used = int.from_bytes(img.read(4), "little")
            self.imp_colors = int.from_bytes(img.read(4), "little")

            # Reading color table if present
            if self.bits_per_pixel <= 8:
                self.color_table = []
                tmp1 = []
                tmp2 = []
                tmp3 = []
                tmp4 = []
                for x in range(self.colors_used):
                    tmp1.append(int.from_bytes(img.read(1), "little"))
                    tmp2.append(int.from_bytes(img.read(1), "little"))
                    tmp3.append(int.from_bytes(img.read(1), "little"))
                    tmp4.append(int.from_bytes(img.read(1), "little"))
                self.color_table.append(tmp1)
                self.color_table.append(tmp2)
                self.color_table.append(tmp3)
                self.color_table.append(tmp4)

            
            # Reading Bitmap image into array
            self.img_arr = []

            for x in range(self.height):
                tmp = []
                for y in range(self.width):
                    tmp.append(int.from_bytes(img.read(self.bits_per_pixel//8), "little"))
                self.img_arr.append(tmp)

            # Printing required data
            print()
            print("File:", file)
            print("Height of Image:", self.height)
            print("Width of Image:", self.width)
            print("Bit Width of Image:", self.bits_per_pixel)
            print("File Size of Image:", self.file_size)
            print("Size of image:", self.image_size)
            print("Offset Size:", self.d_offset)
            print("\n")



    def writeBMP(self, file_name):
        with open(file_name, "wb") as img:

            # File Header Determined by calculation from BMP header
            sign = 'BM'
            offset = 14 + 40 + (4*self.colors_used if self.bits_per_pixel <= 8 else 0)
            file_size = offset + self.height*self.width*self.bits_per_pixel//8
            reserved = 0

            # Writing the file header
            img.write(sign.encode("ascii"))
            img.write(file_size.to_bytes(4, "little"))
            img.write(reserved.to_bytes(4, "little"))
            img.write(offset.to_bytes(4, "little"))

            # Writing BMP header
            img.write(self.hdr_size.to_bytes(4, "little"))
            img.write(self.width.to_bytes(4, "little"))
            img.write(self.height.to_bytes(4, "little"))
            img.write(self.planes.to_bytes(2, "little"))
            img.write(self.bits_per_pixel.to_bytes(2, "little"))
            img.write(self.compression.to_bytes(4, "little"))
            img.write(self.image_size.to_bytes(4, "little"))
            img.write(self.XpixelsperM.to_bytes(4, "little"))
            img.write(self.YpixelsperM.to_bytes(4, "little"))
            img.write(self.colors_used.to_bytes(4, "little"))
            img.write(self.imp_colors.to_bytes(4, "little"))

            # Writing color table if present
            if self.bits_per_pixel <= 8:
                for x in range(self.colors_used):
                    img.write(self.color_table[0][x].to_bytes(1, "little"))
                    img.write(self.color_table[1][x].to_bytes(1, "little"))
                    img.write(self.color_table[2][x].to_bytes(1, "little"))
                    img.write(self.color_table[3][x].to_bytes(1, "little"))

            # Writing the pixel data
            for i in range(self.height):
                for j in range(self.width):
                    tmp = self.img_arr[i][j]
                    img.write(tmp.to_bytes(self.bits_per_pixel//8, "little"))


    # Funciton to filter red color by changing color table value to 0
    def remove_R(self, file_name):
        tmp = self.color_table.copy()
        self.color_table[2] = [0 for x in range(len(self.color_table[2]))]
        self.writeBMP(file_name)
        self.color_table = tmp
    
    # Funciton to filter green color by changing color table value to 0
    def remove_G(self, file_name):
        tmp = self.color_table.copy()
        self.color_table[1] = [0 for x in range(len(self.color_table[1]))]
        self.writeBMP(file_name)
        self.color_table = tmp

    # Funciton to filter blue color by changing color table balue to 0
    def remove_B(self, file_name):
        tmp = self.color_table.copy()
        self.color_table[0] = [0 for x in range(len(self.color_table[0]))]
        self.writeBMP(file_name)
        self.color_table = tmp


if __name__ == "__main__":

    file = # Enter the file name here

    # Reading files
    img = Image(file)

    # Writing BMP file
    new_file = # Enter file name here
    img1.writeBMP(new_file)

    new_file_r = # Enter file name here
    new_file_b = # Enter file name here
    new_file_g = # Enter file name here
    img2.remove_R(new_file_r)
    img2.remove_B(new_file_b)
    img2.remove_G(new_file_g)
