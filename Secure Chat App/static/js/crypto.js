// Generate RSA Key Pair
async function generateRSAKeys() {
    return await window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256",
        },
        true,
        ["encrypt", "decrypt"]
    );
}

async function exportPublicKeyJwk(publicKey) {
    return await window.crypto.subtle.exportKey("jwk", publicKey);
}

async function exportPrivateKeyJwk(privateKey) {
    return await window.crypto.subtle.exportKey("jwk", privateKey);
}

async function importPublicKeyJwk(jwk) {
    return await window.crypto.subtle.importKey(
        "jwk",
        jwk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["encrypt"]
    );
}

async function importPrivateKeyJwk(jwk) {
    return await window.crypto.subtle.importKey(
        "jwk",
        jwk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["decrypt"]
    );
}

async function getOrCreateRSAKeys(storageKey) {
    const stored = localStorage.getItem(storageKey);
    if (stored) {
        try {
            const parsed = JSON.parse(stored);
            const publicKey = await importPublicKeyJwk(parsed.publicKeyJwk);
            const privateKey = await importPrivateKeyJwk(parsed.privateKeyJwk);
            return { publicKey, privateKey };
        } catch (_error) {
            localStorage.removeItem(storageKey);
        }
    }

    const keyPair = await generateRSAKeys();
    const publicKeyJwk = await exportPublicKeyJwk(keyPair.publicKey);
    const privateKeyJwk = await exportPrivateKeyJwk(keyPair.privateKey);
    localStorage.setItem(
        storageKey,
        JSON.stringify({ publicKeyJwk, privateKeyJwk })
    );
    return keyPair;
}

function arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = "";
    for (let i = 0; i < bytes.byteLength; i += 1) {
        binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
}

function base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i += 1) {
        bytes[i] = binary.charCodeAt(i);
    }
    return bytes.buffer;
}

// Generate AES Key
async function generateAESKey() {
    return await window.crypto.subtle.generateKey(
        {
            name: "AES-GCM",
            length: 256,
        },
        true,
        ["encrypt", "decrypt"]
    );
}

async function exportPublicKey(publicKey) {
    const spki = await window.crypto.subtle.exportKey("spki", publicKey);
    return arrayBufferToBase64(spki);
}

async function importPublicKey(publicKeyBase64) {
    return await window.crypto.subtle.importKey(
        "spki",
        base64ToArrayBuffer(publicKeyBase64),
        {
            name: "RSA-OAEP",
            hash: "SHA-256",
        },
        true,
        ["encrypt"]
    );
}

// Encrypt Message with AES
async function encryptMessage(message, aesKey) {
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const encoded = new TextEncoder().encode(message);

    const ciphertext = await window.crypto.subtle.encrypt(
        { name: "AES-GCM", iv: iv },
        aesKey,
        encoded
    );

    return {
        ciphertextBase64: arrayBufferToBase64(ciphertext),
        ivBase64: arrayBufferToBase64(iv.buffer),
    };
}

async function encryptAESKey(aesKey, receiverPublicKeyBase64) {
    const rawAesKey = await window.crypto.subtle.exportKey("raw", aesKey);
    const receiverPublicKey = await importPublicKey(receiverPublicKeyBase64);
    const encryptedKey = await window.crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        receiverPublicKey,
        rawAesKey
    );
    return arrayBufferToBase64(encryptedKey);
}

async function encryptAESKeyWithPublicKey(aesKey, publicKey) {
    const rawAesKey = await window.crypto.subtle.exportKey("raw", aesKey);
    const encryptedKey = await window.crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        publicKey,
        rawAesKey
    );
    return arrayBufferToBase64(encryptedKey);
}

async function decryptAESKey(encryptedKeyBase64, privateKey) {
    const decryptedRawKey = await window.crypto.subtle.decrypt(
        { name: "RSA-OAEP" },
        privateKey,
        base64ToArrayBuffer(encryptedKeyBase64)
    );
    return await window.crypto.subtle.importKey(
        "raw",
        decryptedRawKey,
        {
            name: "AES-GCM",
            length: 256,
        },
        false,
        ["decrypt"]
    );
}

async function decryptMessage(ciphertextBase64, ivBase64, aesKey) {
    const plaintextBuffer = await window.crypto.subtle.decrypt(
        {
            name: "AES-GCM",
            iv: new Uint8Array(base64ToArrayBuffer(ivBase64)),
        },
        aesKey,
        base64ToArrayBuffer(ciphertextBase64)
    );
    return new TextDecoder().decode(plaintextBuffer);
}
