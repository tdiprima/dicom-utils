You can use **`gdcmconv`** or **`dcmtk`** to compress a DICOM file from the command line in Bash.

---

### **🔹 Method 1: Using `gdcmconv` (GDCM - Grassroots DICOM)**
The **GDCM** toolkit provides an easy way to compress DICOM files using lossless JPEG or JPEG 2000.

#### **Lossless JPEG Compression**

```bash
gdcmconv --jpeg -i input.dcm -o compressed.dcm
```

#### **Lossless JPEG 2000 Compression**

```bash
gdcmconv --jpeg2k -i input.dcm -o compressed.dcm
```

#### **RLE (Run-Length Encoding) Compression**

```bash
gdcmconv --rle -i input.dcm -o compressed.dcm
```

> 📌 **Note:** Install GDCM if you don’t have it:  
> **Ubuntu/Debian:** `sudo apt install gdcm-bin`  
> **Mac (Homebrew):** `brew install gdcm`  

---

### **🔹 Method 2: Using `dcmtk` (DICOM Toolkit)**
The **DCMTK** toolkit provides the `dcmcjpeg` tool for compressing DICOM files.

#### **JPEG Lossless Compression**

```bash
dcmcjpeg +tl input.dcm compressed.dcm
```

#### **JPEG 2000 Lossless Compression**

```bash
dcmcjpeg +tj2 input.dcm compressed.dcm
```

> 📌 **Install DCMTK:**  
> **Ubuntu/Debian:** `sudo apt install dcmtk`  
> **Mac (Homebrew):** `brew install dcmtk`

---

### **🔹 Method 3: Using `dcmcjp2k` for JPEG 2000 Compression (DCMTK)**

```bash
dcmcjpls input.dcm compressed.dcm
```

---

### **🔹 Verifying Compression**
After compression, check the DICOM transfer syntax to confirm it’s compressed:

```bash
gdcminfo compressed.dcm | grep "Transfer Syntax"
```

or

```bash
dcmdump compressed.dcm | grep "Transfer Syntax"
```

---

### **🔹 Summary**
| Compression Format | GDCM Command | DCMTK Command |
|-------------------|-------------|--------------|
| JPEG Lossless | `gdcmconv --jpeg -i input.dcm -o compressed.dcm` | `dcmcjpeg +tl input.dcm compressed.dcm` |
| JPEG 2000 | `gdcmconv --jpeg2k -i input.dcm -o compressed.dcm` | `dcmcjpeg +tj2 input.dcm compressed.dcm` |
| RLE | `gdcmconv --rle -i input.dcm -o compressed.dcm` | ❌ Not supported |

---

### **💡 Best Choice?**
- **GDCM (`gdcmconv`)** is easier for JPEG 2000 and RLE compression.
- **DCMTK (`dcmcjpeg`)** is better for standard JPEG compression.

🚀🔥

<br>
