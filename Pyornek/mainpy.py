# isim=input("İsminizi giriniz...")
# # print("Merhaba {}".format(isim))

# sayi1=input("1. sayı")
# sayi2=input("2. sayı")
# toplam=float(sayi1)+float(sayi2)
# print(toplam)

# sayi1=input("1. sayı")
# sayi2=input("2. sayı")
# ortalama=(float(sayi1)+float(sayi2))/2
# print(ortalama)

# vize=input("Vize notunuzu giriniz...")
# final=input("Final notunuzu giriniz...")
# ortalama=(float(vize)*0.4)+(float(final)*0.6)
# print("Ortalama {}".format(ortalama))

# sayi1=input("1. sayı")
# sayi2=input("2. sayı")
# sayi3=input("3. sayı")
# ortalama=(float(sayi1)+float(sayi2)+float(sayi3))/3
# print("Ortalama {}".format(ortalama))

# ortalama=int(input("ortalamanızı giriniz : "))
# if(ortalama>=50):
#     print("Geçtiniz")
# else:
#     print("Kaldınız")

# sayi=int(input("Sayı: "))
# if(sayi%2):
#     print("sayı çift")
# else:
#     print("sayı tek")

# sayi=int(input("Bir adet sayı giriniz : "))
# if(sayi<0):
#     print("Sayı negatif")
# elif(sayi>0):
#     print("Sayı pozitif")
# else:
#     print("Sayı sıfır")

# yas=input("Yaşınızı giriniz : ")
# if(int(yas)<18):
#     print("Ehliyet alamazsınız")
# else:
#     print("Ehliyet alabilirsiniz")

# for i in range(1,101):
#     print(i)
# for i in range(1,101):
#     if i%2==0:
#         print(i)
# for i in range (1,101):
#     if i%2!=0:
#         print(i)

# for i in range(1,101):
#     if i%3==0 and i%5==0:
#         print(i)

# sayi=int(input("Bir sayı giriniz: "))
# for i in range(1,(sayi)+1):
#     print(i)

# kisa=int(input("Kısa kenarı giriniz"))
# uzun=int(input("Uzun kenarı giriniz"))
# alan=kisa*uzun
# cevre=2*(kisa+uzun)
# print("Alan{}".format(alan))
# print("Çevre{}".format(cevre))

# isim=input("Adınızı giriniz: ")
# sayac=0
# while sayac< len(isim):
#     print(isim[sayac])
#     sayac+=1
# else:
#     print("adının harflerini listeledim")
# toplam=0
# sayi1=int(input("Birinci sayıyı giriniz : "))
# sayi2=int(input("ikinci sayıyı giriniz : "))
# for i in range ((sayi1)+1,(sayi2)):
#     toplam+=i
# print("{} ile {} arasındaki sayıların toplamı : {}".format(sayi1,sayi2,toplam))

# sayac=0
# sayi=int(input("Sayı giriniz: "))
# for i in range (2,sayi):
#     if(sayi%i==0):
#         sayac+=1
#         break
# if(sayac!=0):
#     print("Sayı asal değil")
# else:
#     print("Sayı asal")
# sayi=int(input("Bir adet sayı giriniz: "))
# tekt=0
# ciftt=0
# for i in range(1,(sayi)):
#     if(i%2==0):
#         ciftt+=i
#     else:
#         tekt+=i
# print("Tek Sayıların Toplamı: {}".format(tekt))
# print("Çift Sayıların Toplamı: {}".format(ciftt))
# yenimaas=0
# maas=int(input("Maaşınızı giriniz: "))
# zam=int(input("Zam oranını giriniz: "))
# yenimaas=maas+((maas*zam)/100)
# print("zamlı maas",yenimaas)

# def daireAlan(yaricap):
# #     alan=float(yaricap)*float(yaricap)*3.14
# #     print("Alan",alan)
# #     return alan
# # r=input("Yarıçapı giriniz: ")
# # daireAlan(r)

# def dAlan(genislik,yukseklik):
# #     alan=float(genislik)*float(yukseklik)
# #     print("Alan",alan)
# #     return alan
# # gen=input("Genişlik: ")
# # yuk=input("Yükseklik: ")
# #
# # dAlan(gen,yuk)

# from random import  randint
# rand=randint(1,100)
# sayac=0
# while True:
#     sayac+=1
#     sayi=int(input("1 ile 100 arasında sayı giriniz.(0 çıkış): "))
#     if(sayi==0):
#         print("Oyunu iptal ettiniz...")
#         break
#     elif sayi<rand:
#         print("Daha yüksek bir sayı giriniz...")
#         continue
#     elif sayi>rand:
#         print("Daha düşük bir sayı giriniz...")
#         continue
#     else:
#         print("Rastgele seçilen sayı: {}".format(rand))
#         print("Tahmin sayınız: {}".format(sayac))
# def ArtıkYıl(yıl):
#     artık=False
#     if yıl%400==0 or (yıl%4==0 and yıl%100!=0): artık=True
#
#     def YılınGünü(Ay,Gün,Yıl):
#         günler=[31,28,31,30,31,30,31,31,30,31,30,31]
#         if ArtıkYıl(Yıl):
#             günler[1]=29
#         sıra=0
#         for a in range (Ay-1):
#             sıra+=günler[a]
#         sıra+=Gün
#         return sıra
# print(YılınGünü(4,9,2018))
# sayilar=[18,22,15,85,65,30,10,20,32,28,101,5,4,32]
# sayac=0
# for sayi in sayilar:
#     if sayi%5==0:
#         print(str(sayi)+(": 5'in katıdır."))
#         sayac=sayac+1
# else:
#     print("Döngü Bitti...")
# print("5 in katı olan sayı adeti : "+str(sayac))

# def kontrol(str):
#     sayac=0
#     for ch in str:
#         if ch=='ğ':
#             sayac=sayac+1
#             return True
#             break
# metin=input("Metin : ")
# if(kontrol(metin)==True):
#     print("ğ karakteri metinin içinde mevcut")
# else:
#     print("ğ karakteri metinin içinde mevcut değil")
# def ciftMi(x):
#     return x%2==0
# toplam=0
# sayac=0
# baslangic=input("Başlangıç Sayısı: ")
# bitis=input("Bitiş Sayısı: ")
# for sayi in range(int(baslangic),int(bitis)+1):
#     if(ciftMi(int(sayi))):
#         toplam=toplam+sayi
#         sayac=sayac+1
# print("Ortalama: ",(toplam/sayac))

# import tkinter
# nesne=tkinter.Tk()
# nesne.mainloop()

# from tkinter import *
#
# from tkinter import messagebox
# pencere=Tk()
#
# pencere.title("Batuhan")
# pencere.geometry("400x300")
# uygulama=Frame(pencere)
# uygulama.grid()
#
# L1=Label(uygulama,text="Adınızı Girin")
# L1.grid(padx=110,pady=10)
#
# E1=Entry(uygulama,bd=2)
# E1.grid(padx=110,pady=3)
#
# pencere.mainloop()

# from tkinter import *
# from tkinter import messagebox
# pencere=Tk()
# pencere.title("Listview")
# pencere.geometry("400x300")
# uygulama=Frame(pencere)
# uygulama.grid()
# Lb1=Listbox(uygulama)
# Lb1.insert(1,"Python")
# Lb1.insert(2,"cython")
# Lb1.insert(3,"jython")
# Lb1.insert(4,"kython")
# Lb1.grid(padx=110,pady=10)
# pencere.mainloop()
#
# def dAlan(genislik,yukseklik):
#     alan=float(genislik)*float(yukseklik)
#     print("Alan: ",alan)
#     return alan
# gen=input("Genişlik: ")
# yuk=input("Yukseklik : ")
# dAlan(gen,yuk)
# import  random
# liste=["Baba","Anne","Çocuk"]
# print(random.choice(liste))

# def ciftMi(x):
#     return x%2==0
# toplam=0
# sayac=0
# baslangic=input("Başlangıç Sayısı: ")
# bitis=input("Bitiş Sayısı: ")
# for sayi in range(int(baslangic),int(bitis)+1):
#     if(ciftMi(int(sayi))):
#         toplam=toplam+sayi
#         sayac=sayac+1
# print("Ortalama: ",(toplam/sayac))
