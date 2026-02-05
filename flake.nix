{
  description = "Python development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
          };
        };
      in {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            yapf
            pyright
          ];

          buildInputs = with pkgs; [
            python312
            terraform
            terraform-ls
            google-cloud-sdk
            python312Packages.pip
            python312Packages.httpx
            python312Packages.flask
            python312Packages.pytest_8_3
            python312Packages.pytest-mock
            python312Packages.pytest-asyncio
            python312Packages.functions-framework
          ];

          shellHook = ''
            echo "Python ${pkgs.python312.version} environment"
          '';
        };
      }
    );
}
