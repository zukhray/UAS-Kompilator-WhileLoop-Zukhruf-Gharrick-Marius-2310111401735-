# Tugas Proyek Akhir: Representasi Tahapan Kompilasi

**Konstruksi yang Dipilih:** Perulangan / *Looping* (`while`)

## 1. Pattern (Pola Sintaks)
Pola sintaksis didefinisikan menggunakan pendekatan *Backus-Naur Form* (BNF) sederhana:
```text
<while_stmt> ::= "while" "(" <condition> ")" "{" <statements> "}"
<condition>  ::= <identifier> <operator> <value>
<statements> ::= <identifier> "=" <expression>