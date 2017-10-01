function (doc, meta) {
    if (meta.type == "json") {
        emit(doc.city, doc.sales);
    } else {
        emit(["blob"]);
    }
}