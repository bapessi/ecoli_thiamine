let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
argglobal
%argdel
edit ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/dependency.py
argglobal
balt ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/cut_reactions.py
setlocal fdm=expr
setlocal fde=nvim_treesitter#foldexpr()
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=7
setlocal fml=1
setlocal fdn=20
setlocal fen
18
normal! zo
40
normal! zo
42
normal! zo
44
normal! zo
68
normal! zo
70
normal! zo
72
normal! zo
85
normal! zo
86
normal! zo
87
normal! zo
let s:l = 63 - ((1 * winheight(0) + 18) / 37)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 63
normal! 0
tabnext 1
badd +5 ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/dependency.py
badd +29 ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/FBA.py
badd +3 ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/cut_reactions.py
badd +4 ~/Seafile/Bruno/CtrlAB/E\ coli\ lactate/reaction_direction.py
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToOF
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
