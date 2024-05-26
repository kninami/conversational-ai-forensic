chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "fetchData") {
      const tabId = request.tabId;
  
      // Get cookies for the current tab
      chrome.cookies.getAll({name: "lastActiveOrg", url: request.url}, (cookies) => {
        const orgId = cookies[0].value;

        // Execute script to get all hrefs from the current tab
        chrome.scripting.executeScript({
          target: {tabId: tabId},
          func: getAllHrefs
        }, (results) => {
            if (results && results.length > 0) {
                const hrefs = results[0].result;
                const apiUrls = createAPIurls(orgId, hrefs);

                // Fetch data from URLs
                fetchUrls(apiUrls).then(responses => {
                    const jsonArray = responses.map(response => response.data);
                    console.log('Fetched responses:', jsonArray);
                    sendResponse({data: jsonArray});
                });
            }
        });
    });
  
    // Function to be executed in the context of the web page to get all hrefs
    function getAllHrefs() {
    return Array.from(document.querySelectorAll('a[href]')).map(a => a.href).filter(href => href.includes('/chat/'));
    }

    // Function to create api url => /api/organizations/{orgId}/chat_conversations/{chat_id}
    function createAPIurls(orgId, hrefs) {
    const apiArray = [];
    for (const href of hrefs) {
        const match = href.match(/\/chat\/([^\/]+)/);
        if (match) {
            apiArray.push("/api/organizations/"+ orgId + "/chat_conversations/" + match[1])
            }
        }
    return apiArray;
    }
      
    // Function to fetch data from URLs
    async function fetchUrls(urls) {
        const root = "https://claude.ai"
        const responses = [];
        for (const url of urls) {
            try {
                const response = await fetch(root + url);
                if (response.ok) {
                    const json = await response.json();
                    responses.push({url, data: json});
                } else {
                responses.push({url, error: `Error: ${response.statusText}`});
                }
            } catch (error) {
                responses.push({url, error: `Error: ${error.message}`});
            }
        }
        return responses;
    }

      return true; // Keep the message channel open for sendResponse
    }
  });