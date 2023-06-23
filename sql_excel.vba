Option Explicit

Sub Upload()

    ' Upload data from cells B1:F100 to Teradata table "user_work.mytable"

    ' Summary:
    ' This subroutine uploads data from cells B1:F100 to a Teradata table named "user_work.mytable".
    '
    ' Prerequisites:
    ' 1. The Teradata ODBC driver must be installed.
    ' 2. The ADODB library reference must be added to the VBA project.
    '
    ' Steps:
    ' 1. Set the connection string for the Teradata database.
    ' 2. Open a connection to the Teradata database.
    ' 3. Create the table "user_work.mytable" if it does not exist.
    ' 4. Configure the command object for executing SQL INSERT statements.
    ' 5. Loop through the rows to upload data from cells B1:F100.
    ' 6. Append parameter values for the current row to the command object.
    ' 7. Check if a batch is complete and execute the batch if necessary.
    ' 8. Clear parameter values for the next batch.
    ' 9. Execute the remaining batch, if any.
    ' 10. Close the connection to the Teradata database.
    ' 11. Display the total number of batches inserted.
    
    Dim conn As New ADODB.Connection    ' ADODB connection object for database connection
    Dim cmd As New ADODB.Command        ' ADODB command object for executing SQL commands
    Dim i As Long                       ' Loop variable for iterating over rows
    Dim conn_str As String              ' Connection string for the Teradata database
    Const batchSize As Long = 100       ' Number of rows to insert in each batch
    Dim batchCount As Long              ' Total number of batches inserted
    Dim rowCount As Long                ' Number of rows processed in current batch

    conn_str = "Driver={Teradata};DBCName=dbc;Database=user_work;Uid=dbc;Pwd=dbc;"
    conn.Open conn_str                  ' Open the connection to the Teradata database

    ' Create the table if it does not exist
    cmd.ActiveConnection = conn
    cmd.CommandText = "CREATE TABLE IF NOT EXISTS user_work.mytable (Column1 INT, Column2 INT, Column3 INT, Column4 INT, Column5 INT)"
    cmd.Execute

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

Sub QueryAndInsertData()

    ' Query data from "user_work.othertable" and insert into "Sheet issues"
    
    ' Summary:
    ' This subroutine retrieves data from the "user_work.othertable" table in Teradata
    ' and inserts the values into a worksheet named "Sheet issues" in the active workbook.
    '
    ' Prerequisites:
    ' 1. The Teradata ODBC driver must be installed.
    ' 2. The ADODB library reference must be added to the VBA project.
    '
    ' Steps:
    ' 1. Set the connection string and SQL query to retrieve data from the table.
    ' 2. Open a connection to the Teradata database.
    ' 3. Execute the query and retrieve the data into a recordset.
    ' 4. Set the worksheet object to insert the data into.
    ' 5. Set the starting row index for inserting data.
    ' 6. Loop through the recordset and insert the data into the worksheet.
    ' 7. Close the recordset and connection.
    ' 8. Display a message to inform the user that the data has been inserted.
    
    Dim conn As New ADODB.Connection    ' ADODB connection object for database connection
    Dim rs As New ADODB.Recordset       ' ADODB recordset object for storing query results
    Dim conn_str As String              ' Connection string for the Teradata database
    Dim query As String                 ' SQL query to retrieve data
    Dim ws As Worksheet                 ' Worksheet object to insert data into
    Dim row As Long                     ' Row index for inserting data
    
    ' Set the connection string and SQL query
    conn_str = "Driver={Teradata};DBCName=dbc;Database=user_work;Uid=dbc;Pwd=dbc;"
    query = "SELECT * FROM user_work.othertable"
    
    ' Open the connection
    conn.Open conn_str
    
    ' Execute the query and retrieve the data into the recordset
    rs.Open query, conn
    
    ' Set the worksheet to insert the data into
    Set ws = ThisWorkbook.Sheets("Sheet issues")
    
    ' Set the starting row to insert data
    row = 2 ' Assuming the headers are in row 1
    
    ' Loop through the recordset and insert the data into the worksheet
    Do Until rs.EOF
        ws.Cells(row, 1).Value = rs.Fields(0).Value   ' Assuming the first field is in column A
        ws.Cells(row, 2).Value = rs.Fields(1).Value   ' Assuming the second field is in column B
        ws.Cells(row, 3).Value = rs.Fields(2).Value   ' Assuming the third field is in column C
        ' Add more lines as needed for additional fields
        
        rs.MoveNext    ' Move to the next record
        row = row + 1  ' Increment the row index
    Loop
    
    ' Close the recordset and connection
    rs.Close
    conn.Close
    
    ' Inform the user that the data has been inserted
    MsgBox "Data inserted into Sheet issues"
    
End Sub

Sub CompleteTasks()

    ' Call Upload, execute remote script with plink, and call QueryAndInsertData
    
    ' Call the Upload subroutine to upload data to Teradata
    Call Upload
    
    ' Execute the remote script using plink synchronously and wait for it to finish
    Call ExecuteRemoteScriptSync
    
    ' Call the QueryAndInsertData subroutine to query data from Teradata and insert into worksheet
    Call QueryAndInsertData
    
    ' Inform the user that the tasks are completed
    MsgBox "All tasks completed."

End Sub

Sub Upload()
    ' Your Upload subroutine code here
End Sub

Sub ExecuteRemoteScriptSync()
    ' Execute the remote script synchronously using plink and wait for it to finish
    Dim plinkCommand As String
    Dim waitOnReturn As Boolean
    
    ' Set the plink command and wait on return
    plinkCommand = "plink.exe -ssh username@hostname -pw password -m script.txt"
    waitOnReturn = True
    
    ' Execute the plink command synchronously and wait for it to finish
    Shell plinkCommand, vbNormalFocus
    Do While Shell("cmd /c echo", vbHide) <> 0
        DoEvents
    Loop
End Sub

Sub QueryAndInsertData()
    ' Your QueryAndInsertData subroutine code here
End Sub


Sub CheckDataValidation()

    Dim wsSource As Worksheet
    Dim wsTarget As Worksheet
    Dim rng As Range
    Dim cell As Range
    Dim ErrorMsg As String
    
    ' Define the source and target worksheets
    Set wsSource = ThisWorkbook.Sheets("Sheet1")
    Set wsTarget = ThisWorkbook.Sheets("Sheet2")
    
    ' Define the error message
    ErrorMsg = "Your specific error message"
    
    ' Define the range to be checked
    Set rng = wsSource.Range("A1:A" & wsSource.Cells(wsSource.Rows.Count, "A").End(xlUp).Row)
    
    ' Initialize the row number for the target worksheet
    nextRow = wsTarget.Cells(wsTarget.Rows.Count, "A").End(xlUp).Row + 1
    
    ' Check each cell in the range
    For Each cell In rng
        On Error Resume Next
        ' If data validation fails
        If cell.Validation.Value = False Then
            ' Write the cell address and error message to the target worksheet
            wsTarget.Cells(nextRow, "A").Value = cell.Address
            wsTarget.Cells(nextRow, "B").Value = ErrorMsg
            ' Move to the next row in the target worksheet
            nextRow = nextRow + 1
        End If
        On Error GoTo 0
    Next cell

End Sub

