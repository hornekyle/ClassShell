#==================================#
#=== Setup Global Configuration ===#
#==================================#
cmake_minimum_required(VERSION 3.16)
project(ME4750 LANGUAGES "NONE")

include("${CMAKE_SOURCE_DIR}/Tooling/CMake/Package.cmake")

#==============#
#== Includes ==#
#==============#

set(BUILD_INCLUDES
	"Outcomes"
	"Rubrics"
	"Definitions"
	"Questions"
	"Trees"
	"Plots"
	"Order"
	"Solutions"
	"Notes"
	"Invoice"
	"Objectives"
	"LyX"
	"Typst"
	"Toys"
	"Modules"
	"Describe"
	)

foreach(BUILD_FILE IN LISTS BUILD_INCLUDES)
	message(": ${BUILD_FILE}")
	include("${CMAKE_SOURCE_DIR}/Tooling/CMake/${BUILD_FILE}.cmake")
	message(": ${BUILD_FILE}")
endforeach(BUILD_FILE)
