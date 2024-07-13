document.getElementById('fetch').addEventListener('click', () => {
  const fetchButton = document.getElementById('fetch');
  const loadingMessage = document.getElementById('loadingMessage');
  
  // 버튼 비활성화 및 로딩 메시지 표시
  fetchButton.disabled = true;
  fetchButton.style.opacity = '0.5';  // 투명도를 조절하여 비활성화 상태를 시각적으로 표현
  loadingMessage.style.display = 'block';

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const currentTab = tabs[0];
    chrome.runtime.sendMessage({
      action: "fetchData",
      tabId: currentTab.id,
      url: currentTab.url
    }, (response) => {
      const jsonArray = response.data;
      const jsonString = JSON.stringify(jsonArray, null, 2);
      downloadJson(jsonString, 'claude_chat_data.json');
    });
  });
  // 버튼 비활성화 및 로딩 메시지 표시
  fetchButton.disabled = false;
  fetchButton.style.opacity = '1';
  loadingMessage.style.display = 'none';  
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