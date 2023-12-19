"""アニメーション用のgroファイルの最後のフレームだけをとりだす。

```
python3 lastframe.py < 00010-0.gro > 00010-0.last.gro
```

"""
import gromacs

frames = [frame for frame in gromacs.read_gro(sys.stdin)]
gromacs.write_gro(frames[-1], sys.stdout)
