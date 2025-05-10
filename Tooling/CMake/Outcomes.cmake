#==========================================#
#== Create About targets for all modules ==#
#==========================================#

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Objectives.py")
set(OBJECTIVES_SHEET "Tooling/Sheets/Objectives.ods")
set(OBJECTIVES_SHEET_FULL "${CMAKE_SOURCE_DIR}/${OBJECTIVES_SHEET}")
set(MODULES_SHEET "Tooling/Sheets/Modules.ods")
set(MODULES_SHEET_FULL "${CMAKE_SOURCE_DIR}/${MODULES_SHEET}")

execute_process(
	COMMAND
		python "-B" "${SCRIPT_FILE}"
		"${OBJECTIVES_SHEET_FULL}" "--modules"
	OUTPUT_VARIABLE
		MODULES_LIST
	WORKING_DIRECTORY
		"${CMAKE_BINARY_DIR}"
	)

set(SCRIPT_FILE "${CMAKE_SOURCE_DIR}/Tooling/Generators/Outcomes.py")

message("Adding module Outcomes targets:")
add_custom_target("Outcomes" ALL)
foreach(MODULE ${MODULES_LIST})
	file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/Modules/${MODULE}")
	
	set(OUTCOME_FILE "Modules/${MODULE}/Outcomes.csv")
	set(OUTCOME_FILE_FULL "${CMAKE_BINARY_DIR}/${OUTCOME_FILE}")
	
	string(REPLACE "/" "--" OUTCOME_TARGET_CSV ${OUTCOME_FILE})
	string(REPLACE ".csv" "" OUTCOME_TARGET_NAME ${OUTCOME_TARGET_CSV})
	
	set(TARGET_ALERT " :  <source>:${OBJECTIVES_SHEET}∈${MODULE} →  <build>:${OUTCOME_TARGET_CSV}")
	message("${TARGET_ALERT}")
	
	add_custom_command(
		OUTPUT
			"${OUTCOME_FILE_FULL}"
		COMMAND
			"${SCRIPT_FILE}"
		ARGS
			"${OBJECTIVES_SHEET_FULL}"
			"${MODULES_SHEET_FULL}"
			${OUTCOME_FILE_FULL}
		DEPENDS
			"${OBJECTIVES_SHEET_FULL}"
			"${MODULES_SHEET_FULL}"
			"${SCRIPT_FILE}"
		WORKING_DIRECTORY
			"${CMAKE_BINARY_DIR}/Modules/${MODULE}"
		)
	add_custom_target("${OUTCOME_TARGET_NAME}" ALL DEPENDS "${OUTCOME_FILE_FULL}")
	add_dependencies("Outcomes" "${OUTCOME_TARGET_NAME}")
endforeach(MODULE)
message("\nDone!\n")
