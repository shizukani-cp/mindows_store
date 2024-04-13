import PySimpleGUI as pg
import csv, subprocess, shutil, json
pg.set_options(font=(None, 24))
layout = [
    [pg.Input(k="serch_word"), pg.Button("sarch", bind_return_key=True, k="serch"),],
    [pg.Listbox(list(), k="candidate", enable_events=True, size=(50, 10)),],
]
with open("store.csv", "r", encoding="utf-8") as csvf:
    apps = [row for row in csv.reader(csvf)]
win = pg.Window("mindows store", layout, finalize=True)
print([name for _, name in apps])
win["candidate"].update(values=[f"{name} - {user}" for user, name in apps])
while True:
    e, v = win.read()
    if e == None: break
    print(e, v)
    if e == "serch":
        #candidates = [name for _, name in apps if name in v["serch_word"]]
        win["candidate"].update(
            values=[f"{name} - {user}" for user, name in apps if v["serch_word"] in f"{name} - {user}"]
            )
        #print(v["serch_word"], candidates)
    if e == "candidate":
        for i in range(len(apps)):
            if i[1] == v["candidate"]:
                app = i
                break
        if pg.popup_yes_no(f"would you like to install {app[1]} - {app[0]} ?") == "Yes":
            subprocess.run(f"git clone https://github.com/{app[0]}/{app[1]}.git _tmp")
            with open("_tmp/manifest.json", "r", encoding="utf-8") as f:
                app_manifest = json.loads(f.read())
            shutil.copytree("_tmp", f"apps/{app_manifest['uuid']}")
            shutil.copy("_tmp/manifest.json", f"apps/infos/{app_manifest['uuid']}.json")
            shutil.copytree("_tmp", "apps", dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(f"{app_manifest['uuid']}.json"))
            shutil.rmtree("_tmp")
        #apps.index(v["candidate"])
win.close()