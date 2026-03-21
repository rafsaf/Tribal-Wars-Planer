window.twpPlausibleConfig = JSON.parse("{{ plausible_config_json|escapejs }}");

window.plausible = window.plausible || function () {
    (plausible.q = plausible.q || []).push(arguments);
};

window.plausible.init = window.plausible.init || function (options) {
    plausible.o = options || {};
};

function twpNormalizePlausibleUrl(rawUrl) {
    if (!rawUrl) {
        return rawUrl;
    }

    try {
        var parsedUrl = new URL(rawUrl, window.location.origin);
        parsedUrl.pathname = parsedUrl.pathname
            .replace(/\/overview\/[^/?#]+(?=\/|$)/, "/overview/_TOKEN_")
            .replace(/\/planer\/\d+(?=\/|$)/g, "/planer/_OUTLINE_")
            .replace(/\/shipments\/\d+(?=\/|$)/g, "/shipments/_SHIPMENT_")
            .replace(/\/planer-target\/\d+(?=\/|$)/g, "/planer-target/_TARGET_");
        return parsedUrl.toString();
    } catch (error) {
        return rawUrl
            .replace(/\/overview\/[^/?#]+(?=\/|$)/, "/overview/_TOKEN_")
            .replace(/\/planer\/\d+(?=\/|$)/g, "/planer/_OUTLINE_")
            .replace(/\/shipments\/\d+(?=\/|$)/g, "/shipments/_SHIPMENT_")
            .replace(/\/planer-target\/\d+(?=\/|$)/g, "/planer-target/_TARGET_");
    }
}

function twpTransformPlausibleRequest(payload) {
    if (payload.u) {
        payload.u = twpNormalizePlausibleUrl(payload.u);
    }

    if (payload.r) {
        try {
            var referrerUrl = new URL(payload.r, window.location.origin);
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
    var plausibleConfig = window.twpPlausibleConfig || {};

    if (
        window.twpPlausibleBootstrapped ||
        !plausibleConfig.enabled ||
        !plausibleConfig.scriptSrc ||
        !plausibleConfig.endpoint
    ) {
        return;
    }

    window.twpPlausibleBootstrapped = true;

    var plausibleScript = document.createElement("script");
    plausibleScript.async = true;
    plausibleScript.src = plausibleConfig.scriptSrc;
    document.head.appendChild(plausibleScript);

    var plausibleOptions = {
        endpoint: plausibleConfig.endpoint,
        transformRequest: twpTransformPlausibleRequest,
    };

    if (plausibleConfig.captureOnLocalhost) {
        plausibleOptions.captureOnLocalhost = true;
    }

    window.plausible.init(plausibleOptions);
})();