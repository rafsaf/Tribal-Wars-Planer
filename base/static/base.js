


// new_outline, add error to line in code mirror textarea
add_line_error = function (codemirror_id, line) {
        codemirror = $(codemirror_id);
        var codeMirrorEditor = codemirror[0].CodeMirror;
        codeMirrorEditor.addLineClass(parseInt(line), 'wrap', 'line-error');
}

add_first_line_error = function (codemirror_id, line) {
        $(codemirror_id).addClass('CodeMirror-Invalid');
        codemirror = $(codemirror_id);
        var codeMirrorEditor = codemirror[0].CodeMirror;
        codeMirrorEditor.addLineClass(parseInt(line), 'wrap', 'line-error');
        codeMirrorEditor.scrollIntoView(parseInt(line));
}
