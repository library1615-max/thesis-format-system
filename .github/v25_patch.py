from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
marker = '</style>'
css = '''

/* V2.5 - Header contrast refinement */
.siteTitle{
  color:#243B3A;
  font-weight:950;
  text-shadow:0 1px 1px rgba(36,59,58,.16);
}
.titleBox .siteSub{
  color:#343A3A;
  font-weight:500;
  line-height:1.75;
}
.titleBox .siteSub + .siteSub{
  color:#4A5050;
}
'''
if '/* V2.5 - Header contrast refinement */' not in s:
    if marker not in s:
        raise SystemExit('style closing tag not found')
    s = s.replace(marker, css + '\n' + marker, 1)
p.write_text(s, encoding='utf-8')
