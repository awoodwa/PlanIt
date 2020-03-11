import os
from PlanIt import planitapp


if __name__ == "__planitapp__":
    #port = int(os.environ.get("PORT", 5000))
    planitapp.app.run(debug=True)  #(host="0.0.0.0", port=port)
