Dim V_x As Integer
Dim V_y As Integer
Dim V_result As Integer
Input V_x
Input V_y
V_result = V_x + V_y
Print V_result
Function F_calculate (V_a , V_b , V_c)
Dim V_sum As Integer
Dim V_difference As Integer
Dim V_product As Integer
V_sum = V_a + V_b
V_difference = V_a - 10
V_product = V_b * V_c
F_calculate = V_sum
End Function
Function F_display (V_message , V_value , V_dummy)
Dim V_temp1 As Integer
Dim V_temp2 As Integer
Dim V_temp3 As Integer
V_temp1 = V_value
V_temp2 = V_message
V_temp3 = V_temp1 + V_temp2
Print V_temp3
End Function