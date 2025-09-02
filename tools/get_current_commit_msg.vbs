' This code asks the user about the commit msg & saves it to ./tools/cm.i
commit_msg = InputBox("Leaving it empty will set the commit message to NULL","Your commit Message")
if f = "" Then
    f = "NULL"
End If

' File Interaction
commit_msg_path = "cm.i"
Set FSO = CreateObject("Scripting.FileSystemObject")
Set objFile = FSO.CreateTextFile(commit_msg_path, True)
objFile.Write commit_msg
objFile.Close