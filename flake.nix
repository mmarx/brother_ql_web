{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    utils.url = "github:gytis-ivaskevicius/flake-utils-plus";
  };

  outputs = inputs @ {
    self,
    utils,
    ...
  }:
    utils.lib.mkFlake {
      inherit self inputs;

      outputsBuilder = channels: let
        pkgs = channels.nixpkgs;
      in {
        devShells.default = pkgs.mkShell {
          nativeBuildInputs = [
            pkgs.python3
            pkgs.black
            pkgs.mypy
            pkgs.fontconfig
            pkgs.python3Packages.bottle
            pkgs.python3Packages.brother-ql
            pkgs.python3Packages.flake8
            pkgs.python3Packages.jinja2
            pkgs.python3Packages.pep8-naming
            pkgs.python3Packages.pylibdmtx
            pkgs.python3Packages.python-barcode
            pkgs.python3Packages.requests
            pkgs.python3Packages.setuptools-scm
            pkgs.python3Packages.types-pillow
            pkgs.python3Packages.types-requests
          ];
        };

        formatter = pkgs.alejandra;
      };
    };
}
# Local Variables:
# apheleia-formatter: alejandra
# End:
