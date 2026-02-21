import fitz

doc = fitz.open(r'c:\Users\user\Documents\ALEX\HOME\apartment-app\docs\לאטי-2279-הסכם-חתום.pdf')
for i in range(26, 30):
    print(f"---PAGE {i+1}---")
    try:
        print(doc[i].get_text())
    except:
        pass
doc.close()
