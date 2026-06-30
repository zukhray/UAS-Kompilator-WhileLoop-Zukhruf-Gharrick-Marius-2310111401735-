class WhileCompiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.label_counter = 1

    def new_label(self):
        lbl = f"L{self.label_counter}"
        self.label_counter += 1
        return lbl

    def lexical_analysis(self):
        # 1. TAHAP LEKSIKAL: Memecah string input menjadi kumpulan token
        # Menambahkan spasi di sekitar simbol agar mudah di-split
        code = self.source_code.replace('(', ' ( ').replace(')', ' ) ')
        code = code.replace('{', ' { ').replace('}', ' } ')
        tokens = code.split()
        return tokens

    def syntax_semantic_analysis(self, tokens):
        # 2 & 3. TAHAP SINTAKSIS & SEMANTIK: Membentuk AST dan validasi dasar
        
        # Validasi keyword awal
        if tokens[0] != 'while':
            raise SyntaxError("Error Sintaks: Bukan struktur perulangan 'while'.")
        
        try:
            # Mencari indeks simbol penting
            idx_open_paren = tokens.index('(')
            idx_close_paren = tokens.index(')')
            idx_open_brace = tokens.index('{')
            idx_close_brace = tokens.index('}')
            
            # Ekstraksi kondisi dan isi blok kode (body)
            condition_tokens = tokens[idx_open_paren+1 : idx_close_paren]
            body_tokens = tokens[idx_open_brace+1 : idx_close_brace]
            
            condition = " ".join(condition_tokens)
            body = " ".join(body_tokens)
            
            # CEK SEMANTIK SEDERHANA: Pastikan kondisi punya operator perbandingan yang valid
            valid_operators = ['<', '>', '==', '<=', '>=', '!=']
            if not any(op in condition_tokens for op in valid_operators):
                raise ValueError("Error Semantik: Kondisi perulangan tidak valid (tidak ada operator perbandingan).")
            
            # Membentuk Abstract Syntax Tree (AST) sederhana dalam bentuk dictionary
            ast = {
                'type': 'while_loop',
                'condition': condition,
                'body': body
            }
            return ast
            
        except ValueError as e:
            # Menangkap error semantik yang kita buat, atau error list.index jika simbol tidak lengkap
            if "Error Semantik" in str(e):
                raise e
            raise SyntaxError("Error Sintaks: Struktur kurung tidak lengkap.")

    def generate_tac(self):
        # 4. TAHAP GENERASI KODE ANTARA (TAC)
        tokens = self.lexical_analysis()
        ast = self.syntax_semantic_analysis(tokens)
        
        label_start = self.new_label()
        label_end = self.new_label()
        
        tac = []
        tac.append(f"{label_start}:")
        tac.append(f"ifFalse {ast['condition']} goto {label_end}")
        tac.append(f"{ast['body']}")
        tac.append(f"goto {label_start}")
        tac.append(f"{label_end}:")
        
        return "\n".join(tac)

# --- Contoh Penggunaan (Bisa langsung di-run) ---
if __name__ == "__main__":
    # Source code yang akan dikompilasi
    source = "while ( x < 10 ) { x = x + 1 }"
    print(f"=== SOURCE CODE ===\n{source}\n")
    
    compiler = WhileCompiler(source)
    
    print("=== 1. ANALISIS LEKSIKAL (TOKENS) ===")
    tokens = compiler.lexical_analysis()
    print(tokens, "\n")
    
    print("=== 2 & 3. ANALISIS SINTAKSIS & SEMANTIK (AST) ===")
    ast = compiler.syntax_semantic_analysis(tokens)
    print(ast, "\n")
    
    print("=== 4. GENERASI KODE ANTARA (TAC) ===")
    print(compiler.generate_tac())