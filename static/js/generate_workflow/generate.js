/**
 * Created by dfitzgerald on 8/11/15.
 */
$(document).ready(function(){
    var getParametersForProgramURL = '/swiftseq/generate-workflow/generate/get-parameters-for-program/';

    $('.option-checkbox').change(function(){
        /* Get the Step ID, hook it up to respective program panel */
        var stepId = $(this).data('stepid');
        var $panel = $('div.panel-program[data-stepid="' + stepId + '"]');
        $panel.slideToggle(150);
    });

    $('div.programset').each(function(){
        var stepId = $(this).parent('div.panel-program').data('stepid');
        $(this).ProgramSet({stepId: stepId});
    });

    $('span.add-program').click(function(){
        var stepId = $(this).data('stepid');
        var $panelProgram = $('div.panel-program[data-stepid="'+stepId+'"]');
        $('<div>').addClass('panel-body programset').appendTo($panelProgram).ProgramSet({stepId: parseInt(stepId)});
    });

    $('#submitbutton').click(function(){
        $('input').removeAttr('disabled');
        $('<iframe>').attr({
            src: '/swiftseq/generate-workflow/process-workflow/?' + $('form').serialize(),
            style: 'display:none'
        }).appendTo($('body'));
        window.setTimeout(function(){window.location.replace('/swiftseq/generate-workflow/download-complete/');}, 500);
    });
});