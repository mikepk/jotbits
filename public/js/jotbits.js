//jb namespace
var jotbits = new (function() {

    // some init stuff
    var dmp = new diff_match_patch();
    dmp.Diff_Timeout = 1.0;
    dmp.Diff_EditCost = 4.0;

    var base_text = ''; //$("#note").val();
    var new_text = '';

    this.save_data = function() {
        $.ajax({type:'PUT', data:{'text':$('#note').val()}});
    }

    this.diff = function() {
        new_text = $("#note").val();
        return dmp.diff_main(base_text, new_text);
    }

    this.delta = function(diff) {
        return dmp.diff_toDelta(diff);
    }

    this.to_diff = function(delta) {
        return dmp.diff_fromDelta(base_text, delta);
    }

    this.generate_patch = function(diff) {
        // new_text = $("#note").val();
        var patch_list = dmp.patch_make(base_text, new_text, diff);
        patch_text = dmp.patch_toText(patch_list);
        return patch_text;
    }

    //init function
    $(document).ready(function() {
        base_text = $("#note").val();
    });
});