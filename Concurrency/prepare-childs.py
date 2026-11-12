#!/usr/bin/env python3
import os
import re
from glob import glob
from jinja2 import Template

def main():
    # テンプレートの読み込み
    with open('template.mdp', 'r') as f:
        template_str = f.read()
    template = Template(template_str)

    # *bar/*K という形式のディレクトリをすべて探す
    target_dirs = glob("*bar/*K")

    for d in target_dirs:
        # パスから温度(T)と圧力(P)を抽出
        # 例: 8000bar/160K -> P=8000, T=160
        match_p = re.search(r'(\d+)bar', d)
        match_t = re.search(r'(\d+)K', d)
        
        # ディレクトリ名が異常でなければ
        if match_p and match_t:
            p_val = match_p.group(1)
            t_val = match_t.group(1)
            
            output_path = os.path.join(d, 'continue.mdp')
            
            # もしすでにあれば上書きはしない。(日付が変わるとmakeがまた動いてしまう)
            if os.path.exists(output_path):
                print(f"Skipped (P={p_val}, T={t_val})")
                continue

            # レンダリング
            rendered_content = template.render(T=t_val, P=p_val)
            
            # ファイル書き出し
            with open(output_path, 'w') as f:
                f.write(rendered_content)
            print(f"Generated {output_path} (P={p_val}, T={t_val})")

if __name__ == "__main__":
    main()


