let snapshots = [];
let allSnapshots = [];

var removeAllCookies = function () {

    if (!chrome.cookies) {
        chrome.cookies = chrome.experimental.cookies;
    }

    var removeCookie = function (cookie) {
        var url = "http" + (cookie.secure ? "s" : "") + "://" + cookie.domain + cookie.path;
        chrome.cookies.remove({"url": url, "name": cookie.name});
    };

    chrome.cookies.getAll({}, function (all_cookies) {
        var count = all_cookies.length;
        for (var i = 0; i < count; i++) {
            removeCookie(all_cookies[i]);
        }
    });

    console.log('Successfully remove all cookies!');
};

function getSecondLevelDomain(hostname) {
    const specialTLDs = ['co.uk', 'gov.uk', 'ac.uk', 'org.uk'];
    
    const parts = hostname.split('.');
  
    if (parts.length < 2) {
      return null;
    }
  
    const lastPart = parts.slice(-2).join('.');
    if (specialTLDs.includes(lastPart)) {
      return parts.slice(-3).join('.');
    }
  
    return parts.slice(-2).join('.');
}


document.getElementById('saveSnapshot').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({
        currentWindow: true,
        active: true
    });

    const url = new URL(tab.url);
    const domain = getSecondLevelDomain(url.hostname);
    // const website = new URL(tab.url);
    // const cookies = await chrome.cookies.getAll({ url: url.origin });
    const cookies = await chrome.cookies.getAll({ domain: domain });
    const snapshot = { timestamp: Date.now(), hash: MD5(JSON.stringify(cookies)), cookies};
    snapshots.push(snapshot);
    updateTable();
});


document.getElementById('clear').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({
        currentWindow: true,
        active: true
    });

    const url = new URL(tab.url);
    const cookies = await chrome.cookies.getAll({ url: url.origin });

    // 遍历并删除每个 cookie
    for (const cookie of cookies) {
        await chrome.cookies.remove({
            url: url.origin + cookie.path,
            name: cookie.name
        });
    }
});


document.getElementById('saveAllSnapshot').addEventListener('click', async () => {
    const cookies = await chrome.cookies.getAll({});
    const snapshot = { timestamp: Date.now(), hash: MD5(JSON.stringify(cookies)), cookies};
    allSnapshots.push(snapshot);
    updateAllTable();
});


document.getElementById('clearAll').addEventListener('click', async () => {
    removeAllCookies();
});


document.getElementById('compareSnapshots').addEventListener('click', () => {
    const selectRows = Array.from(document.querySelectorAll('#snapshotBody tr.selected'));

    if (selectRows.length == 2) {
        const [first, second] = selectRows.map(row => snapshots[row.dataset.index]);
        compareSnapshots(first, second);
    } else {
        alert("Please select exactly two snapshots.");
    }
});

document.getElementById('compareAllSnapshots').addEventListener('click', () => {
    const selectRows = Array.from(document.querySelectorAll('#snapshotAllBody tr.selected'));

    if (selectRows.length == 2) {
        const [first, second] = selectRows.map(row => allSnapshots[row.dataset.index]);
        compareSnapshots(first, second);
    } else {
        alert("Please select exactly two snapshots.");
    }
    
});


const dialog = document.getElementById('dialog');
const dialogContent = document.getElementById('dialogContent');
const closeDialog = document.getElementById('closeDialog');

closeDialog.addEventListener('click', function() {
    dialog.style.display = 'none';
});

function updateTable() {
    const tbody = document.getElementById('snapshotBody');
    tbody.innerHTML = '';
    snapshots.forEach((snapshot, index) => {
        const row = document.createElement('tr');
        row.dataset.index = index;
        row.innerHTML = `
            <td>${new Date(snapshot.timestamp).toLocaleString()}</td>
            <td>${snapshot.hash || null}</td>
            <td>${snapshot.cookies.length || 0}</td>
            <td><button class="viewBtn">Look</button></td>
        `;

        row.addEventListener('click', () => {
            row.classList.toggle('selected');
        });
        tbody.appendChild(row);
    });

    tbody.addEventListener('click', function(event) {
        if (event.target.classList.contains('viewBtn')) {
            const rowIndex = event.target.closest('tr').dataset.index;
            const rowData = snapshots[rowIndex];
    
            // 使用 <pre> 标签来保持格式
            dialogContent.innerHTML = `<pre>${JSON.stringify(rowData, null, 2)}</pre>`;
            
            // 添加CSS样式
            dialogContent.style.backgroundColor = '#f9f9f9';
            dialogContent.style.border = '1px solid #ccc';
            dialogContent.style.borderRadius = '4px';
            dialogContent.style.padding = '10px';
            dialogContent.style.overflowX = 'auto'; // 处理长文本的滚动条
            dialog.style.display = 'block';
        }
    });
}

function updateAllTable() {
    const tbody = document.getElementById('snapshotAllBody');
    tbody.innerHTML = '';
    allSnapshots.forEach((snapshot, index) => {
        const row = document.createElement('tr');
        row.dataset.index = index;
        row.innerHTML = `
        <td>${new Date(snapshot.timestamp).toLocaleString()}</td>
        <td>${snapshot.hash || null}</td>
        <td>${snapshot.cookies.length || 0}</td>
        <td><button class="viewBtn">Look</button></td>
        `;

        row.addEventListener('click', () => {
            row.classList.toggle('selected');
        });
        tbody.appendChild(row);
    });

    tbody.addEventListener('click', function(event) {
        if (event.target.classList.contains('viewBtn')) {
            const rowIndex = event.target.closest('tr').dataset.index;
            const rowData = allSnapshots[rowIndex];
    
            // 使用 <pre> 标签来保持格式
            dialogContent.innerHTML = `<pre>${JSON.stringify(rowData, null, 2)}</pre>`;
            
            // 添加CSS样式
            dialogContent.style.backgroundColor = '#f9f9f9';
            dialogContent.style.border = '1px solid #ccc';
            dialogContent.style.borderRadius = '4px';
            dialogContent.style.padding = '10px';
            dialogContent.style.overflowX = 'auto'; // 处理长文本的滚动条
            dialog.style.display = 'block';
        }
    });
}


function compareSnapshots(snapshot1, snapshot2) {
    const cookies1 = snapshot1.cookies;
    const cookies2 = snapshot2.cookies;

    const cookies2Names = new Set(cookies2.map(cookie => cookie.domain + '' + cookie.name));
    const comparsionResults = { change: {}, add: [], delete: [] };
    
    cookies2.forEach(cookie => {

        const cookie1 = cookies1.find(c => c.name === cookie.name && c.domain === cookie.domain);

        if (cookie1) {
            // Compare cookies
            if (MD5(JSON.stringify(cookie)) !== MD5(JSON.stringify(cookie1))) {
                comparsionResults.change[cookie.name] = {};
                for (let key in cookie) {
                    if (cookie[key] !== cookie1[key]) {
                        comparsionResults.change[cookie.name][key] = [cookie[key], cookie1[key]];
                    }
                }
            }
        } else {
            comparsionResults.add.push(cookie);
        }
    });

    cookies1.forEach(cookie => {
        if (!cookies2Names.has(cookie.domain + '' + cookie.name)) {
            comparsionResults.delete.push(cookie);
        }
    });

    displayComparsionResults(snapshot1.hash, snapshot2.hash, comparsionResults);
}




let count = 0;

function displayComparsionResults(hash1, hash2, results) {
    const comparsionBody = document.getElementById('comparsionBody');
    comparsionBody.innerHTML = '';
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${count++}</td>
        <td>${hash1}</td>
        <td>${hash2}</td>
        <td><button class="viewBtn">Look</button></td>
    `

    // row.addEventListener('click', () => {
    //     toggleDetails(JSON.stringify(results, null, 2));
    // });

    comparsionBody.appendChild(row);

    comparsionBody.addEventListener('click', function(event) {
        if (event.target.classList.contains('viewBtn')) {
            const rowIndex = event.target.closest('tr').dataset.index;
            // 使用 <pre> 标签来保持格式
            dialogContent.innerHTML = `<pre>${JSON.stringify(results, null, 2)}</pre>`;
            // 添加CSS样式
            dialogContent.style.backgroundColor = '#f9f9f9';
            dialogContent.style.border = '1px solid #ccc';
            dialogContent.style.borderRadius = '4px';
            dialogContent.style.padding = '10px';
            dialogContent.style.overflowX = 'auto'; // 处理长文本的滚动条
            dialog.style.display = 'block';
        }
    });
}


function toggleDetails(details) {
    const detailsDiv = document.getElementById('comparsionDetails');
    if (detailsDiv.innerHTML == details) {
        detailsDiv.innerHTML = '';
    } else {
        detailsDiv.innerHTML = `<pre>${details}</pre>`
    }
}

// Close details when clicking outside
document.addEventListener('click', (event) => {
    const comparisonDiv = document.getElementById('comparsionDetails');
    if (!comparisonDiv.contains(event.target) && event.target.closest('#comparsionTable') === null) {
        comparisonDiv.innerHTML = '';
    }
});


// Intercept
let isIntercepting = false;
let requests= [];
let requestGroups = [];

const startBtn = document.getElementById('startBtn');
const pauseBtn = document.getElementById('pauseBtn');
const clearBtn = document.getElementById('clearBtn');
const requestGroupBody = document.getElementById('requestGroupBody');
const requestBody = document.getElementById('requestBody');

// Start Event
startBtn.addEventListener('click', () => {
    if (!isIntercepting) {

        requests = [];

        startBtn.style.backgroundColor = '#0056b3'; // 更深的颜色
        pauseBtn.style.backgroundColor = ''; // 恢复默认颜色
        
        chrome.runtime.sendMessage({ action: "startIntercept" });
        isIntercepting = true;
    }
});

// Pause Event
pauseBtn.addEventListener('click', () => {
    if (isIntercepting) {

        pauseBtn.style.backgroundColor = '#0056b3'; // 更深的颜色
        startBtn.style.backgroundColor = ''; // 恢复默认颜色

        chrome.runtime.sendMessage({ action: "pauseIntercept"});
        isIntercepting = false;

        requestGroups.push({timestamp: Date.now(), hash: MD5(JSON.stringify(requests)), requests});
        updateRequestGroup();
        requests = [];
    }
});

// Clear Event
clearBtn.addEventListener('click', () => {
    requests = [];
    requestGroups = [];
    const tbody = document.getElementById('requestGroupBody');
    tbody.innerHTML = '';
});

// receieve the request data from background
chrome.runtime.onMessage.addListener((message) => {
    if (message.action === "captureRequest") {
        requests.push(message.data);
    }
});

function updateRequestGroup() {

    const tbody = document.getElementById('requestGroupBody');
    tbody.innerHTML = '';
    requests = Array.from(new Set(requests));
    requestGroups.forEach((request, index) => {
        const row = document.createElement('tr');
        row.dataset.index = index;
        row.innerHTML = `
            <td>${new Date(request.timestamp).toLocaleString()}</td>
            <td>${request.hash || null}</td>
            <td>${request.requests.length || 0}</td>
            <td><button class="viewBtn">Look</button></td>
        `
        row.addEventListener('click', () => {
            row.classList.toggle('selected');
        });
        tbody.appendChild(row);
    });

    tbody.addEventListener('click', function(event) {
        if (event.target.classList.contains('viewBtn')) {
            const rowIndex = event.target.closest('tr').dataset.index;
            const rowData = requestGroups[rowIndex].requests;
    
            // 使用 <pre> 标签来保持格式
            dialogContent.innerHTML = `<pre>${JSON.stringify(rowData, null, 2)}</pre>`;
            
            // 添加CSS样式
            dialogContent.style.backgroundColor = '#f9f9f9';
            dialogContent.style.border = '1px solid #ccc';
            dialogContent.style.borderRadius = '4px';
            dialogContent.style.padding = '10px';
            dialogContent.style.overflowX = 'auto'; // 处理长文本的滚动条
            dialog.style.display = 'block';
        }
    });
}


const updateBtn = document.getElementById('updateBtn');
updateBtn.addEventListener('click', async () => {

    const tableBody = document.querySelector('#cookieTable tbody');

    const [tab] = await chrome.tabs.query({
        currentWindow: true,
        active: true
    });

    const url = new URL(tab.url);
    const domain = getSecondLevelDomain(url.hostname);

    const cookies = await chrome.cookies.getAll({ domain: domain });

    tableBody.innerHTML = ''; // 清空表格
    cookies.forEach(cookie => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${cookie.name}</td>
            <td>${cookie.domain}</td>
            <td>${cookie.path}</td>
            <td>${cookie.value}</td>
            <td>
                <button class="toggle-cookie" data-name="${cookie.name}" data-value="${encodeURIComponent(JSON.stringify(cookie))}" style="background-color: red; color: white;">Disable</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
    updateToggleButtons();
});

function updateToggleButtons() {
    const buttons = document.querySelectorAll('.toggle-cookie');
    buttons.forEach(button => {
        const cookie = JSON.parse(decodeURIComponent(button.getAttribute('data-value')));
        const domain = cookie.domain.startsWith('.') ? cookie.domain.slice(1) : cookie.domain; // 去掉开头的点
        const url = "http" + (cookie.secure ? "s" : "") + "://" + domain + cookie.path;
        const cookieName = button.getAttribute('data-name');
        button.onclick = function() {
            
            const isEnabled = button.textContent === 'Disable';
            if (isEnabled) {
                // 删除 cookie
                chrome.cookies.remove({"url": url, "name": cookieName}, function() {
                    button.textContent = 'Enable';
                    button.style.backgroundColor = 'blue';
                    chrome.storage.local.remove(cookieName);
                });
            } else {
                const c = {
                    url: url,
                    name: cookie.name,
                    value: cookie.value,
                    // domain: cookie.domain,
                    path: cookie.path,
                    secure: cookie.secure,
                    httpOnly: cookie.httpOnly
                };

                // 开启 cookie
                chrome.cookies.set(c, function(c) {
                    if (chrome.runtime.lastError) {
                        console.error(chrome.runtime.lastError);
                    } else {
                        button.textContent = 'Disable';
                        button.style.backgroundColor = 'red';
                        chrome.storage.local.set({ [cookieName]: true });
                    }
                });
            }
        };
    });
}