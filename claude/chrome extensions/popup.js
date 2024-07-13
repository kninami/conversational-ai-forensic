document.getElementById('fetch').addEventListener('click', () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    chrome.runtime.sendMessage({
      action: "fetchData",
      tabId: currentTab.id,
      url: currentTab.url
    }, (response) => {
      const jsonArray = response.data;
      console.log("jsonArray")
      console.log(jsonArray);
      const jsonString = JSON.stringify(jsonArray, null, 2);
      console.log("jsonString")
      console.log(jsonString);
      downloadJson(jsonString, 'claude_chat_data.json');
    });
  });
});

function downloadJson(content, fileName) {
  const blob = new Blob([content], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}