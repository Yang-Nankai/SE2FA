// chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
//     if (message.action === "addClickIntercept") {
//         const {selector, reqNum} = message;
        
//         alert(`Succfully add the listener on ${selector}`);
//         console.log("[2FA EXTENSION] Now waiting for capture the request and response ...");
    
//         const element = document.querySelector(selector);

//         if (element) {
//             const handleClick = () => {
//                 chrome.runtime.sendMessage({ action: "collectIntercept", reqNum });
//             };
//             element.addEventListener("click", handleClick);
//             console.log(`Listener set for element with selector: ${selector}`);
//         }
//     }
// });
      