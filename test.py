import global_var as gl
import test2

print(gl.point_cnt)
gl.point_cnt = 5555
test2.test()
print(gl.point_cnt)
gl.point_cnt = 6666
test2.test()
print(gl.point_cnt)