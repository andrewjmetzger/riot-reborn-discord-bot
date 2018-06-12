# Recover deleted records

## Restore a recently deleted record

If a record was accidentally removed with the [`leave` command](../commands/leave.md), an administrator with Editor access to the spreadsheet can attempt to undo the deletion.

----------

From the menu at the top of the window, click **File** &gt; **Version history** &gt; **See version history**

![Using the File menu to access the version history of a spreadsheet in Google Sheets.](../.gitbook/assets/image%20%282%29.png)

In the Version history pane on the right, **select an older version**, which contains the record you want to restore. 

{% hint style="info" %}
The version you restore will generally be created by the bot, so look for its service account username, as defined in your server's [`credentials.json`](../administration/credentials.md) \(in this case, `bender`\).
{% endhint %}

![The version history panel, with an older version of the spreadsheet selected.](../.gitbook/assets/image%20%284%29.png)

Notice the affected records become **highlighted** in the preview to the left. 

![Selecting a revision displays the affected records, shown here with a red outline.](../.gitbook/assets/image%20%285%29.png)

Click **Restore this version** in the upper-left corner 

![](../.gitbook/assets/image%20%287%29.png)

