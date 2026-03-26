window.twpPlausibleConfig = JSON.parse("{{ plausible_config_json|escapejs }}");

window.plausible = window.plausible || function () {
    (plausible.q = plausible.q || []).push(arguments);
};

window.plausible.init = window.plausible.init || function (options) {
    plausible.o = options || {};
};

function twpReplacePlausiblePath(pathname) {
    return pathname
        .replace(/\/overview\/[^/?#]+(?=\/|$)/, "/overview/_TOKEN_")
        .replace(/\/activate\/[^/?#]+(?=\/|$)/, "/activate/_ACTIVATION_KEY_")
        .replace(/\/reset\/[^/]+\/[^/?#]+(?=\/|$)/, "/reset/_UID_/_TOKEN_")
        .replace(/\/planer\/\d+(?=\/|$)/g, "/planer/_OUTLINE_")
        .replace(/\/planer-target\/\d+(?=\/|$)/g, "/planer-target/_TARGET_")
        .replace(/\/shipments\/\d+(?=\/|$)/g, "/shipments/_SHIPMENT_");
}

function twpReplacePlausibleSearch(search) {
    return (search || "")
        .replace(/([?&])token=[^&#]*/g, "$1token=_TOKEN_")
        .replace(/([?&])activation_key=[^&#]*/g, "$1activation_key=_ACTIVATION_KEY_");
}

function twpNormalizePlausibleUrl(rawUrl) {
    if (!rawUrl) {
        return rawUrl;
    }

    try {
        const parsedUrl = new URL(rawUrl, window.location.origin);
        parsedUrl.pathname = twpReplacePlausiblePath(parsedUrl.pathname);
        parsedUrl.search = twpReplacePlausibleSearch(parsedUrl.search);
        return parsedUrl.toString();
    } catch (error) {
        console.error("Failed to normalize Plausible URL", rawUrl, error);
        throw error;
    }
}

function twpTransformPlausibleRequest(payload) {
    if (payload.u) {
        payload.u = twpNormalizePlausibleUrl(payload.u);
    }

    if (payload.r) {
        try {
            const referrerUrl = new URL(payload.r, window.location.origin);
            if (referrerUrl.hostname === window.location.hostname) {
                payload.r = twpNormalizePlausibleUrl(payload.r);
            }
        } catch (error) {
        }
    }

    if (payload.p && payload.p.url) {
        payload.p.url = twpNormalizePlausibleUrl(payload.p.url);
    }

    return payload;
}

(function bootstrapTwpPlausible() {
    const plausibleConfig = window.twpPlausibleConfig || {};

    if (
        window.twpPlausibleBootstrapped ||
        !plausibleConfig.enabled ||
        !plausibleConfig.scriptSrc ||
        !plausibleConfig.endpoint
    ) {
        return;
    }

    window.twpPlausibleBootstrapped = true;

    const plausibleScript = document.createElement("script");
    plausibleScript.async = true;
    plausibleScript.src = plausibleConfig.scriptSrc;
    document.head.appendChild(plausibleScript);

    const plausibleOptions = {
        endpoint: plausibleConfig.endpoint,
        transformRequest: twpTransformPlausibleRequest,
    };

    if (plausibleConfig.captureOnLocalhost) {
        plausibleOptions.captureOnLocalhost = true;
    }

    window.plausible.init(plausibleOptions);
})();

window.twpTrack = function (eventName, props) {
    if (typeof window.plausible !== "function") {
        return;
    }
    if (props && Object.keys(props).length > 0) {
        window.plausible(eventName, { props: props });
        return;
    }
    window.plausible(eventName);
};