const socket = io();

const savedUsername = localStorage.getItem("username");
if (!savedUsername) {
    window.location.href = "/";
}
const username = savedUsername || "Unknown";
const userBadge = document.getElementById("userBadge");
const meAvatar = document.getElementById("meAvatar");
const receiverInput = document.getElementById("receiver");
const activeChatName = document.getElementById("activeChatName");
const headerName = document.getElementById("headerName");
const peerAvatar = document.getElementById("peerAvatar");
const headAvatar = document.getElementById("headAvatar");
const messageFeed = document.getElementById("messageFeed");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("sendBtn");
let myPrivateKey = null;
let myPublicKey = null;
let historyTimer = null;

userBadge.textContent = username;
meAvatar.textContent = username.charAt(0).toUpperCase();

function syncReceiverUI() {
    const receiver = receiverInput.value.trim() || "Secure Contact";
    const initial = receiver.charAt(0).toUpperCase();
    activeChatName.textContent = receiver;
    headerName.textContent = receiver;
    peerAvatar.textContent = initial;
    headAvatar.textContent = initial;
}

function appendMessage({ from, to, encrypted_message, direction }) {
    const row = document.createElement("div");
    row.className = `message-row ${direction}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    const body = document.createElement("p");
    body.textContent = encrypted_message;

    const meta = document.createElement("span");
    meta.className = "meta";
    meta.textContent = `${from} -> ${to}`;

    bubble.appendChild(body);
    bubble.appendChild(meta);
    row.appendChild(bubble);
    messageFeed.appendChild(row);
    messageFeed.scrollTop = messageFeed.scrollHeight;
}

function appendSystemMessage(text) {
    appendMessage({
        from: "System",
        to: username,
        encrypted_message: text,
        direction: "incoming",
    });
}

function clearMessages() {
    messageFeed.innerHTML = "";
}

async function getRecipientPublicKey(recipient) {
    return await new Promise((resolve) => {
        socket.emit("get_public_key", { username: recipient }, (response) => {
            resolve((response || {}).public_key || null);
        });
    });
}

async function fetchHistory(withUser) {
    return await new Promise((resolve) => {
        socket.emit(
            "get_history",
            { username: username, with_user: withUser },
            (response) => {
                resolve((response || {}).messages || []);
            }
        );
    });
}

async function decryptHistoryMessage(msg) {
    let wrappedKey = null;

    if (msg.to === username) {
        wrappedKey = msg.encrypted_key;
    } else if (msg.from === username) {
        wrappedKey = msg.encrypted_key_sender || msg.encrypted_key;
    }

    if (!wrappedKey || !myPrivateKey) {
        return null;
    }

    try {
        const aesKey = await decryptAESKey(wrappedKey, myPrivateKey);
        return await decryptMessage(msg.encrypted_message, msg.iv, aesKey);
    } catch (_error) {
        return null;
    }
}

async function loadHistory() {
    const receiver = receiverInput.value.trim();
    if (!receiver || !myPrivateKey) {
        return;
    }

    const messages = await fetchHistory(receiver);
    clearMessages();

    if (!messages.length) {
        appendSystemMessage("No previous encrypted messages with this user.");
        return;
    }

    for (const msg of messages) {
        const plaintext = await decryptHistoryMessage(msg);
        if (!plaintext) {
            continue;
        }

        const direction = msg.from === username ? "outgoing" : "incoming";
        appendMessage({
            from: msg.from,
            to: msg.to,
            encrypted_message: plaintext,
            direction,
        });
    }
}

async function initializeKeys() {
    try {
        const keyPair = await getOrCreateRSAKeys(`secure_chat_keys_${username}`);
        myPrivateKey = keyPair.privateKey;
        myPublicKey = keyPair.publicKey;
        const myPublicKeyBase64 = await exportPublicKey(myPublicKey);
        socket.emit("register_user", {
            username: username,
            public_key: myPublicKeyBase64,
        });
    } catch (error) {
        appendSystemMessage("Failed to initialize encryption keys.");
        console.error(error);
    }
}

receiverInput.addEventListener("input", () => {
    syncReceiverUI();
    clearTimeout(historyTimer);
    historyTimer = setTimeout(() => {
        loadHistory();
    }, 350);
});

receiverInput.addEventListener("blur", () => {
    loadHistory();
});

syncReceiverUI();

(async () => {
    await initializeKeys();
    await loadHistory();
})();

sendBtn.onclick = async function () {
    const message = messageInput.value.trim();
    const receiver = receiverInput.value.trim();

    if (!message || !receiver) {
        return;
    }

    if (!myPrivateKey || !myPublicKey) {
        appendSystemMessage("Encryption keys not ready yet.");
        return;
    }

    const receiverPublicKey = await getRecipientPublicKey(receiver);
    if (!receiverPublicKey) {
        appendSystemMessage("Recipient not found or not online.");
        return;
    }

    const aesKey = await generateAESKey();
    const encryptedData = await encryptMessage(message, aesKey);
    const encryptedKey = await encryptAESKey(aesKey, receiverPublicKey);
    const encryptedKeySender = await encryptAESKeyWithPublicKey(aesKey, myPublicKey);

    const payload = {
        from: username,
        to: receiver,
        encrypted_message: encryptedData.ciphertextBase64,
        encrypted_key: encryptedKey,
        encrypted_key_sender: encryptedKeySender,
        iv: encryptedData.ivBase64,
    };

    socket.emit("send_message", payload);
    appendMessage({
        from: username,
        to: receiver,
        encrypted_message: message,
        direction: "outgoing",
    });
    messageInput.value = "";
};

messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendBtn.click();
    }
});

socket.on("receive_message", function (data) {
    if (data.from === username || data.to !== username) {
        return;
    }

    (async () => {
        try {
            const aesKey = await decryptAESKey(data.encrypted_key, myPrivateKey);
            const plaintext = await decryptMessage(data.encrypted_message, data.iv, aesKey);
            appendMessage({
                from: data.from,
                to: data.to,
                encrypted_message: plaintext,
                direction: "incoming",
            });
        } catch (error) {
            appendSystemMessage("Failed to decrypt an incoming message.");
            console.error(error);
        }
    })();
});

socket.on("error", function (data) {
    if (data && data.message) {
        appendSystemMessage(data.message);
    }
});
