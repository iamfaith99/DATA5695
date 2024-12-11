{
  description = "A Python 3.12 environment with Poetry, Quarto, Numpy, Scipy, Matplotlib, JAX, PyYAML, IPython, JupyterLab, and Tectonic";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, ... }: let
    systems = [ "x86_64-darwin" "aarch64-darwin" ];
    lib = nixpkgs.lib;
  in
  {
    packages = lib.genAttrs systems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (final: prev: {
            curio = prev.curio.overrideAttrs (oldAttrs: {
              doCheck = false;
            });
          })
        ];
      };
      pythonEnv = pkgs.python312.withPackages (pythonPackages: with pythonPackages; [
        pandas
        numpy
        scipy
        matplotlib
        jax
        pyyaml
        ipython
        jupyterlab
      ]);
    in
    {
      default = pkgs.mkShell {
        buildInputs = [
          pythonEnv
          pkgs.poetry     # Add Poetry to the environment
          pkgs.quarto     # Add Quarto to the environment
          pkgs.tectonic   # Add Tectonic (LaTeX distribution) to the environment
          pkgs.texlive.combined.scheme-full  # Add Texlive medium scheme to include pdflatex
        ];
      };
    });

    devShells = lib.genAttrs systems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [
          (final: prev: {
            curio = prev.curio.overrideAttrs (oldAttrs: {
              doCheck = false;
            });
          })
        ];
      };
      pythonEnv = pkgs.python312.withPackages (pythonPackages: with pythonPackages; [
        pandas
        numpy
        scipy
        matplotlib
        jax
        pyyaml
        ipython
        jupyterlab
      ]);
    in
    {
      default = pkgs.mkShell {
        buildInputs = [
          pythonEnv
          pkgs.poetry     # Add Poetry to the environment
          pkgs.quarto     # Add Quarto to the environment
          pkgs.tectonic   # Add Tectonic (LaTeX distribution) to the environment
          pkgs.texlive.combined.scheme-full # Add Texlive medium scheme to include pdflatex
        ];
      };
    });
  };
}
