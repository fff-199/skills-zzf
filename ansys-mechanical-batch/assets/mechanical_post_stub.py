"""
Optional Mechanical-internal script stub.

Use this only after the outer Workbench batch loop is already stable.
The preferred first version is still:

1. parameterized .wbpj
2. Workbench input/output parameters
3. batch solve through RunWB2.exe
"""


def main():
    analyses = ExtAPI.DataModel.Project.Model.Analyses
    if analyses.Count == 0:
        raise Exception("No analyses found in Mechanical model.")

    analysis = analyses[0]
    solution = analysis.Solution

    # Future extension points:
    # deformation = solution.AddTotalDeformation()
    # stress = solution.AddEquivalentStress()
    # solution.Solve()
    # solution.EvaluateAllResults()

    ExtAPI.Log.WriteMessage("Mechanical post stub executed.")


main()
