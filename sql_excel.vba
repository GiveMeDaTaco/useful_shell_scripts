Option Explicit

Sub Upload()

    ' Upload data from cells B1:F100 to Teradata table "user_work.mytable"
    
    Dim conn As New ADODB.Connection    ' ADODB connection object for database connection
    Dim cmd As New ADODB.Command        ' ADODB command object for executing SQL commands
    Dim i As Long                       ' Loop variable for iterating over rows
    Dim conn_str As String              ' Connection string for the Teradata database
    Const batchSize As Long = 100       ' Number of rows to insert in each batch
    Dim batchCount As Long              ' Total number of batches inserted
    Dim rowCount As Long                ' Number of rows processed in current batch
    
    conn_str = "Driver={Teradata};DBCName=dbc;Database=user_work;Uid=dbc;Pwd=dbc;"
    conn.Open conn_str                  ' Open the connection to the Teradata database
    
    ' Configure the command object
    With cmd
        .ActiveConnection = conn         ' Associate the command with the connection
        .CommandText = "INSERT INTO user_work.mytable VALUES (?,?,?,?,?)"    ' SQL INSERT statement
        .CommandType = adCmdText         ' Set the command type as text
        .Parameters.Refresh              ' Refresh the parameters collection
    End With
    
    ' Loop through the rows to upload data
    For i = 1 To 100
        ' Append parameter values for the current row
        cmd.Parameters(1).AppendChunk Cells(i, 2).Value    ' Parameter 1 value
        cmd.Parameters(2).AppendChunk Cells(i, 3).Value    ' Parameter 2 value
        cmd.Parameters(3).AppendChunk Cells(i, 4).Value    ' Parameter 3 value
        cmd.Parameters(4).AppendChunk Cells(i, 5).Value    ' Parameter 4 value
        cmd.Parameters(5).AppendChunk Cells(i, 6).Value    ' Parameter 5 value
        
        rowCount = rowCount + 1
        
        ' Check if a batch is complete
        If rowCount = batchSize Then
            ' Execute the batch
            cmd.Execute
            
            ' Reset the row count and increment batch count
            rowCount = 0
            batchCount = batchCount + 1
            
            ' Clear parameter values for the next batch
            For j = 1 To 5
                cmd.Parameters(j).Value = Empty                ' Reset parameter value
                cmd.Parameters(j).AppendChunk Empty            ' Clear parameter data
            Next j
        End If
    Next i
    
    ' Execute the remaining batch, if any
    If rowCount > 0 Then
        cmd.Execute
        batchCount = batchCount + 1
    End If
    
    conn.Close                          ' Close the connection to the Teradata database
    
    ' Display the total number of batches inserted
    MsgBox "Total batches inserted: " & batchCount
End Sub
