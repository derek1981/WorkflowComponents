FOR %%A IN (%*) DO (
     ECHO BATCH ARG: %%A
)

"C:/Program Files/Java/jdk1.8.0_144/bin/java.exe" -cp C:\Users\Peter\WorkflowsAndTetrad\WorkflowComponents\CustomLibraries\tetrad-gui-6.5.4-launch.jar -jar C:\Users\Peter\WorkflowsAndTetrad\WorkflowComponents\TetradDiscretize\dist\TetradDiscretize.jar %*
