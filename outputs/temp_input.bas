Dim V_x As Integer
Dim V_y As Integer
Dim V_result As Integer
Input V_x
Input V_y
If grt ( V_x , V_y ) , grt ( V_y And 0 ) Then
    V_result = F_average(V_x , V_y , 0)
    Print V_result
End If
If eq ( V_x , 0 ) , eq ( V_y Or 0 ) Then
    Print "Zero"
End If
V_result = V_x * V_y
Print V_result
Function F_average (V_a , V_b , V_dummy)
Dim V_sum As Integer
Dim V_count As Integer
V_sum = V_a + V_b
V_count = V_sum
V_result = V_sum / V_count
End Function