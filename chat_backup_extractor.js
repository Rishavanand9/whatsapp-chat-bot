// Function to extract text content from a chat item
function extractDataFromChatItem(chatItem) {
    console.log("Extracting data from chat item", chatItem);
    const textContent = chatItem.querySelector('.selectable-text.copyable-text')?.textContent?.trim() || '';

    // Extract date and time
    const dateDiv = chatItem.closest('div[role="row"]').previousElementSibling;
    const date = dateDiv?.querySelector('._ao3e')?.textContent?.trim() || '';
    const timeElement = chatItem.querySelector('.x1rg5ohu.x16dsc37');
    const time = timeElement?.textContent?.trim() || '';

    // Extract PDF link
    const pdfElement = chatItem.querySelector('div[title^="Download"]');
    const pdfLink = pdfElement ? pdfElement.title.split('"')[1] : '';

    // Extract image link (blob URL)
    const imageElement = chatItem.querySelector('img[src^="blob:"]');
    const imageLink = imageElement ? imageElement.src : '';

    const senderElement = chatItem?.childNodes?.[1]?.childNodes?.[2]?.childNodes?.[0]?.children?.[0]?.children?.[0]?.innerText;
    sender = senderElement || 'You';

    console.log(`Extracted sender: "${sender}"`);
    console.log(`Extracted text: "${textContent}", date: "${date}", time: "${time}", PDF: "${pdfLink}", image blob: "${imageLink}", sender: "${sender}"`);
    return { text: textContent, date, time, pdfLink, imageLink, sender };
}

// Function to backup chat content
function backupChatContent() {
    console.log("Starting chat content backup");
    const chatRootDiv = document.getElementsByClassName("x3psx0u xwib8y2 xkhd6sd xrmvbpv")[0];
    if (!chatRootDiv) {
        console.error("Chat root div not found");
        return;
    }
    console.log("Chat root div found");

    const chatItems = Array.from(chatRootDiv.querySelectorAll('.message-in, .message-out'));
    console.log(`Found ${chatItems.length} chat items`);

    const backupData = chatItems.map(item => extractDataFromChatItem(item));
    console.log(`Extracted data from ${backupData.length} items`);

    // Filter out empty entries
    const filteredData = backupData.filter(item => item.text !== '' || item.imageLink !== '');
    console.log(`Filtered data contains ${filteredData.length} non-empty items`);

    // Create a JSON representation of the backup
    const backupJSON = JSON.stringify(filteredData, null, 2);
    console.log("Created JSON representation of backup");

    // Log the backup to console
    console.log("Chat Backup (JSON):");
    console.log(backupJSON);

    // Save the JSON to a file (this will work in a browser environment)
    const blob = new Blob([backupJSON], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'chat_backup.json';
    a.click();
    URL.revokeObjectURL(url);
}

// Run the backup function
backupChatContent();
