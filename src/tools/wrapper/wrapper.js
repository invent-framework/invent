const builder = document.getElementById("builder");
const save = document.getElementById("save");
const load = document.getElementById("load");

window.addEventListener("message", (event) => {
    if (event.source === builder.contentWindow){
        const data = event.data;

        switch (data.type) {
            case "save-response":
                console.log(data.data);
                localStorage.setItem("data", JSON.stringify(data.data));
                break;
        }
    }
});

save.addEventListener("click", () => {
    builder.contentWindow.postMessage({
        type: "save-request"
    }, "*");
});

load.addEventListener("click", () => {
    const data = JSON.parse(localStorage.getItem("data"));

    builder.contentWindow.postMessage({
        type: "load-request",
        data: {
            app: data.app && JSON.parse(data.app),
            datastore: data.datastore && JSON.parse(data.datastore),
            blocks: data.blocks && JSON.parse(data.blocks),
            media: {}
        }
    }, "*");
});